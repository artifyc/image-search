TABLE_NAME_QA="images_qa"
MAX_IMAGES=50
RESPONSE_ATTRIBUTE_LIST="user_id,image_id,tags,#p"
EXPRESSION_ATTRIBUTE_NAMES={"#p":"path"}
DYNAMODB = "dynamodb"
LAST_EVALUATED_KEY = "LastEvaluatedKey"
ITEMS= "Items"
TAGS = "tags"
SORT = "Sort"
IMAGE_COUNT = "Image_Count"
SORT_OPTIONS = {"price":"price_index","rating":"rating_index"}
SORT_ATTRIBUTES = {"price_index":"price_index_const", "rating_index":"rating_index_const"}
PRICE_INDEX_CONST = "1"
#Request Attributes
SORT_TYPES={}