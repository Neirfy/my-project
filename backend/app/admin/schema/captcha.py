from common.schema import SchemaBase


class CaptchaSchemaBase(SchemaBase):
    image_type: str
    image: str
