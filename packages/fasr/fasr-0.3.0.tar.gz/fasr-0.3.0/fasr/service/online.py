from asyncio import Queue
from pathlib import Path
import asyncio
import traceback
from urllib.parse import parse_qs
from typing import Literal, List

from loguru import logger
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, Field, ConfigDict

from fasr.config import registry
from fasr.data import AudioBytesStream, AudioChunk, AudioToken
from fasr.models.stream_asr.base import StreamASRModel
from fasr.models.stream_vad.base import StreamVADModel
from fasr.models.punc.base import PuncModel
from .schema import AudioChunkResponse, TranscriptionResponse


class RealtimeASRService(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="ignore"
    )

    host: str = Field("127.0.0.1", description="服务地址")
    port: int = Field(27000, description="服务端口")
    device: Literal["cpu", "cuda", "mps"] | None = Field(None, description="设备")
    asr_model_name: Literal[
        "stream_sensevoice", "stream_paraformer.torch", "stream_paraformer.onnx"
    ] = Field("stream_paraformer.torch", description="流式asr模型")
    asr_checkpoint_dir: str | Path | None = Field(
        None,
        description="asr模型路径",
    )
    asr_model: StreamASRModel = Field(None, description="asr模型")
    vad_model_name: Literal["stream_fsmn.torch", "stream_fsmn.onnx"] = Field(
        "stream_fsmn.torch", description="流式vad模型"
    )
    vad_model: StreamVADModel = Field(None, description="vad模型")
    vad_checkpoint_dir: str | Path | None = Field(
        None,
    )
    vad_chunk_size_ms: int = Field(100, description="音频分片大小")
    vad_end_silence_ms: int = Field(500, description="vad判定音频片段结束最大静音时间")
    vad_threshold: float = Field(
        0.6,
        description="vad判定阈值, 取值范围0~1，值越大，则需要更大声音量来触发vad，噪音环境下建议设置更高的阈值",
        le=1,
        ge=0,
    )
    vad_db_threshold: int = Field(
        -100,
        description="vad音量阈值,值越大，则需要更大音量来触发vad，噪音环境下建议设置更高的阈值",
    )
    punc_model_name: Literal["ct_transformer"] | None = Field(
        None, description="标点模型"
    )
    punc_model: PuncModel = Field(None, description="标点模型")
    punc_checkpoint_dir: str | Path | None = Field(
        None,
    )
    sample_rate: int = Field(16000, description="音频采样率")
    bit_depth: int = Field(16, description="音频位深")
    channels: int = Field(1, description="音频通道数")

    def setup(self):
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(
            f"Start online ASR Service on {self.host}:{self.port}, device: {self.device}"
        )
        logger.info(
            f"ASR Model: {self.asr_model_name}, VAD Model: {self.vad_model_name}, Punc Model: {self.punc_model_name or 'None'}"
        )
        logger.info(
            f"VAD Config: chunk_size_ms: {self.vad_chunk_size_ms}, end_silence_ms: {self.vad_end_silence_ms}, threshold: {self.vad_threshold}, db_threshold: {self.vad_db_threshold}"
        )

        self.asr_model: StreamASRModel = registry.stream_asr_models.get(
            self.asr_model_name
        )()
        self.asr_model.from_checkpoint(
            checkpoint_dir=self.asr_checkpoint_dir,
            device=self.device,
        )
        self.vad_model: StreamVADModel = registry.stream_vad_models.get(
            self.vad_model_name
        )(
            chunk_size_ms=self.vad_chunk_size_ms,
            max_end_silence_time=self.vad_end_silence_ms,
            speech_noise_thres=self.vad_threshold,
            db_threshold=self.vad_db_threshold,
        )
        self.vad_model.from_checkpoint(
            checkpoint_dir=self.vad_checkpoint_dir,
            device=self.device,
        )
        if self.punc_model_name is not None:
            self.punc_model: PuncModel = registry.punc_models.get(
                self.punc_model_name
            )()
            self.punc_model.from_checkpoint(
                checkpoint_dir=self.punc_checkpoint_dir,
                device=self.device,
            )

        @app.websocket("/asr/realtime")
        async def transcribe(ws: WebSocket):
            try:
                # 解析请求参数
                await ws.accept()
                query_params = parse_qs(ws.scope["query_string"].decode())
                itn = query_params.get("itn", ["false"])[0].lower() == "true"
                model = query_params.get("model", ["paraformer"])[0].lower()
                chunk_size = int(self.vad_chunk_size_ms * self.sample_rate / 1000)
                logger.info(f"itn: {itn}, chunk_size: {chunk_size}, model: {model}")
                queue = Queue()
                tasks = []
                tasks.append(asyncio.create_task(self.vad_task(ws, span_queue=queue)))
                tasks.append(
                    asyncio.create_task(self.asr_task(ws=ws, span_queue=queue))
                )
                await asyncio.gather(
                    *tasks,
                )
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(
                    f"Unexpected error: {e}\nCall stack:\n{traceback.format_exc()}"
                )
                await ws.close()
            finally:
                logger.info("Cleaned up resources after WebSocket disconnect")

        uvicorn.run(app, host=self.host, port=self.port, ws="wsproto")

    async def vad_task(self, ws: WebSocket, span_queue: Queue):
        logger.info("start vad task")
        bytes_buffer = AudioBytesStream(
            sample_rate=self.sample_rate, chunk_size_ms=self.vad_chunk_size_ms
        )
        while True:
            raw_data = await ws.receive()
            bytes_data = raw_data.get("bytes", None)
            if bytes_data is None:
                logger.warning("Received data is None")
                continue
            chunks: List[AudioChunk] = bytes_buffer.push(bytes_data)
            for chunk in chunks:
                for segment_chunk in self.vad_model.detect_chunk(chunk=chunk):
                    segment_chunk: AudioChunk
                    if segment_chunk.vad_state != "segment_mid":
                        await self.send_vad_response(
                            "",
                            ws,
                            segment_chunk.vad_state,
                            start_time=segment_chunk.start_ms,
                            end_time=segment_chunk.end_ms,
                        )
                    await span_queue.put(segment_chunk)

    async def asr_task(self, span_queue: Queue, ws: WebSocket):
        final_text = ""
        start_time = None
        while True:
            span: AudioChunk = await span_queue.get()
            if start_time is None:
                start_time = span.start_ms
            is_last = span.vad_state == "segment_end"
            if is_last:
                end_time = span.end_ms
                for token in self.asr_model.transcribe_chunk(chunk=span):
                    final_text += token.text
                    await self.send_asr_response(token.text, ws, "interim_transcript")
                if self.punc_model is not None:
                    final_text = self.punc_model.restore(final_text).text
                await self.send_asr_response(
                    final_text,
                    ws,
                    "final_transcript",
                    start_time=start_time,
                    end_time=end_time,
                )
                final_text = ""
                start_time = None
            else:
                for token in self.asr_model.transcribe_chunk(chunk=span):
                    token: AudioToken
                    final_text += token.text
                    await self.send_asr_response(token.text, ws, "interim_transcript")
            span_queue.task_done()

    async def send_asr_response(
        self,
        text: str,
        ws: WebSocket,
        state: str,
        start_time: float = None,
        end_time: float = None,
    ):
        text = text.strip()
        if len(text) == 1 and text in ["嗯", "啊"]:
            return
        if len(text) > 0:
            response = TranscriptionResponse(
                data=AudioChunkResponse(
                    text=text, state=state, start_time=start_time, end_time=end_time
                )
            )
            await ws.send_json(response.model_dump())
            logger.info(f"asr state: {state}, text: {text}")

    async def send_vad_response(
        self,
        text: str,
        ws: WebSocket,
        state: str,
        start_time: float = None,
        end_time: float = None,
    ):
        response = TranscriptionResponse(
            data=AudioChunkResponse(
                text=text, state=state, start_time=start_time, end_time=end_time
            )
        )
        await ws.send_json(response.model_dump())
        logger.info(f"vad state: {state}")
