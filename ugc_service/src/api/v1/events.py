import logging
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, HTTPException, Depends

from core import get_settings
from kafka_ugc.producer import get_producer
from models import EventModel

router = APIRouter()
settings = get_settings()


@router.post('/send_event', response_model=HTTPStatus, summary='Add event to Kafka')
async def send_event(event: EventModel, producer: AIOKafkaProducer = Depends(get_producer)) -> int:
    topic = settings.topics.get(event.event_name)
    if not topic:
        logging.error(f'%s not found', event.event_name)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='event_name not found')
    await producer.send_and_wait(
        topic=topic,
        key='+'.join((event.user_id, event.data.movie_id)),
        value=event.data.value,
    )
    return HTTPStatus.CREATED
