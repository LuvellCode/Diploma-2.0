from django.apps import AppConfig
from django.conf import settings
import joblib
import logging


class TrollRecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'troll_recognition'
    _model_name = settings.MODEL_PATH
    model = None  # глобальна змінна для збереження моделі

    def ready(self):
        logger = logging.getLogger('django')
        logger.info(f"\nLoading the pickle object (CatBoost model) in memory: {self._model_name}...")

        if TrollRecognitionConfig.model is None:
            TrollRecognitionConfig.model = joblib.load(self._model_name)
            logger.info("Pickle Model was successfully loaded.")
        else:
            logger.info("Model already exists... Skipped.")
        logger.info("\n")