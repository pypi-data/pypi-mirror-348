import os
import hashlib

from ximilar.client.constants import *
from ximilar.client import RecognitionClient


PRODUCT_ENDPOINT = "product/v2/product/"
IMAGE_ENDPOINT = "product/v2/image/"
COLLECTION_ENDPOINT = "product/v2/collection/"
PRODUCT_SET_ENDPOINT = "product/v2/set/"

class ProductClient(RecognitionClient):
    """
    Ximilar API Client for Products management.
    """

    def __init__(
        self, token, endpoint=ENDPOINT, workspace=DEFAULT_WORKSPACE, max_image_size=0, resource_name=PRODUCTS_MANAGEMENT
    ):
        super().__init__(
            token=token,
            endpoint=endpoint,
            workspace=workspace,
            max_image_size=max_image_size,
            resource_name=resource_name,
        )

    def create_product(self, name, customer_product_id, product_collection, verified=True, product_set=None, meta_data=None):
        data = {NAME: name, "customer_product_id": customer_product_id, "product_collection": product_collection, "verified": verified}

        if meta_data:
            data[META_DATA] = meta_data

        if product_set:
            data["product_set"] = product_set

        product_json = self.post(PRODUCT_ENDPOINT, data=data, params=self.add_workspace(None, None))
        if ID not in product_json:
            return None, {STATUS: "unexpected error"}
        return Product(self.token, self.endpoint, self.workspace, product_json), RESULT_OK

    def create_image(self, record, name, product, meta_data={}, md5s=[]):
        assert product

        record = self._create_image_data(record, True, True, False, meta_data)

        record[NAME] = name
        record["product"] = product

        if "base64" in record and len(md5s):
            md5h = hashlib.md5(record["base64"].encode("utf-8")).hexdigest()
            if md5h in md5s:
                return None, {STATUS: "skipped"}

        image_json = self.post(IMAGE_ENDPOINT, data=record)
        if ID not in image_json:
            return None, {STATUS: "unexpected error"}
        return ProductImage(self.token, self.endpoint, self.workspace, image_json), RESULT_OK

    def get_product_set(self, product_set_id):
        product_set_json = self.get(PRODUCT_SET_ENDPOINT + product_set_id)
        if ID not in product_set_json:
            return None, {STATUS: "unexpected error"}
        return ProductSet(self.token, self.endpoint, self.workspace, product_set_json), RESULT_OK

    def get_product_set_by_name(self, name, product_collection):
        product_set_json = self.get(PRODUCT_SET_ENDPOINT + "?name=" + name + "&product_collection=" + product_collection)
        if RESULTS not in product_set_json or len(product_set_json[RESULTS]) == 0:
            return None, {STATUS: "unexpected error"}
            
        # Find exact name match
        for product_set in product_set_json[RESULTS]:
            if product_set[NAME] == name:
                return ProductSet(self.token, self.endpoint, self.workspace, product_set), RESULT_OK

        return None, {STATUS: "unexpected error"}

    def create_product_set(self, name, product_collection, year, parent=None):
        data = {NAME: name, "product_collection": product_collection, "workspace": self.workspace, "year": year}
        if parent:
            data["parent"] = parent
        product_set_json = self.post(PRODUCT_SET_ENDPOINT, data=data)

        if "make a unique set" in str(product_set_json):
            existing_set, status = self.get_product_set_by_name(name, str(product_collection))
            if existing_set:
                return existing_set, RESULT_OK

        if ID not in product_set_json:
            return None, {STATUS: "unexpected error"}
        return ProductSet(self.token, self.endpoint, self.workspace, product_set_json), RESULT_OK
    
    def add_product_to_set(self, product_set_id, product_id, product_collection):
        data = {"product_set": product_set_id, "workspace": self.workspace, "product_collection": product_collection}
        return self.put(PRODUCT_ENDPOINT + product_id, data=data)

    def get_product(self, product_id):
        product_json = self.get(PRODUCT_ENDPOINT + product_id)
        if ID not in product_json:
            return None, {STATUS: "Product with this id not found!"}
        return Product(self.token, self.endpoint, self.workspace, product_json), RESULT_OK

    def get_image(self, image_id):
        image_json = self.get(IMAGE_ENDPOINT + image_id)
        if ID not in image_json:
            return None, {STATUS: "Image with this id not found!"}
        return ProductImage(self.token, self.endpoint, self.workspace, image_json), RESULT_OK

    def remove_product(self, product_id):
        return self.delete(PRODUCT_ENDPOINT + product_id)

    def remove_image(self, image_id):
        return self.delete(IMAGE_ENDPOINT + image_id)

    def get_images_url(self, page_url, product=None, name=None):
        url = (
            page_url.replace(self.endpoint, "").replace(self.endpoint.replace("https", "http"), "")
            if page_url
            else IMAGE_ENDPOINT + "?page=1"
        )
        if product is not None:
            url = url + "&product=" + str(product)
        if name is not None:
            url = url + "&name=" + str(name)
        return url

    def get_all_products(
        self, page_url=None, product_collection=None, name=None, customer_product_id=None, collection_type=None, product_set=None
    ):
        url = self.get_products_url(page_url, product_collection=product_collection, name=name, customer_product_id=customer_product_id, collection_type=collection_type, product_set=product_set)

        products, status = self.get_all_paginated_items(url)
        if not products and status[STATUS] == STATUS_ERROR:
            return None, status
        return [Product(self.token, self.endpoint, self.workspace, p_json) for p_json in products], RESULT_OK

    def get_all_images(self, product=None):
        url = IMAGE_ENDPOINT
        if product is not None:
            url = url + "?product=" + str(product)

        images, status = self.get_all_paginated_items(url)
        if not images and status[STATUS] == STATUS_ERROR:
            return None, status

        return [ProductImage(self.token, self.endpoint, self.workspace, i_json) for i_json in images], RESULT_OK

    def get_images_by_name(self, page_url, name=None):
        url = self.get_images_url(page_url, name=name)
        result = self.get(url)
        return (
            [ProductImage(self.token, self.endpoint, self.workspace, i_json) for i_json in result[RESULTS]],
            result[NEXT],
            {"count": result["count"], STATUS: "ok"},
        )

    def get_products_url(
        self,
        page_url=None,
        product_collection=None,
        name=None,
        customer_product_id=None,
        collection_type=None,
        ordering=None,
        empty=None,
        product_set=None,
    ):
        url = (
            page_url.replace(self.endpoint, "").replace(self.endpoint.replace("https", "http"), "")
            if page_url
            else PRODUCT_ENDPOINT + "?page=1"
        )

        if page_url is not None:
            return url
        if name is not None:
            url += "&search=" + str(name)
        if product_collection is not None:
            url += "&product_collection=" + str(product_collection)
        if customer_product_id is not None:
            url += "&customer_product_id=" + str(customer_product_id)
        if collection_type is not None:
            url += "&collection_type=" + str(collection_type)
        if ordering is not None:
            url += "&ordering=" + str(ordering)
        if empty is not None:
            url += "&empty=true"
        if product_set is not None:
            url += "&product_set=" + str(product_set)
        return url

    def get_sets_url(
        self,
        page_url=None,
        product_collection=None,
        name=None,
        parent_set=None,
        ordering=None,
    ):
        url = (
            page_url.replace(self.endpoint, "").replace(self.endpoint.replace("https", "http"), "")
            if page_url
            else PRODUCT_SET_ENDPOINT + "?page=1"
        )

        if page_url is not None:
            return url
        if name is not None:
            url += "&search=" + str(name)
        if product_collection is not None:
            url += "&product_collection=" + str(product_collection)
        if parent_set is not None:
            url += "&parent_set=" + str(parent_set)
        if ordering is not None:
            url += "&ordering=" + str(ordering)
        return url

    def get_all_sets(
        self,
        page_url=None,
        product_collection=None,
        name=None,
        parent_set=None,
        ordering=None,
    ):
        url = self.get_sets_url(page_url, product_collection, name, parent_set, ordering)

        sets, status = self.get_all_paginated_items(url)
        if not sets and status[STATUS] == STATUS_ERROR:
            return None, status
        return [ProductSet(self.token, self.endpoint, self.workspace, s_json) for s_json in sets], RESULT_OK

    def get_products(
        self,
        page_url=None,
        product_collection=None,
        name=None,
        customer_product_id=None,
        collection_type=None,
        ordering=None,
        empty=None,
        product_set=None,
    ):
        url = self.get_products_url(
            page_url, product_collection, name, customer_product_id, collection_type, ordering, empty, product_set
        )
        result = self.get(url)
        return (
            [Product(self.token, self.endpoint, self.workspace, product_json) for product_json in result[RESULTS]],
            result[NEXT],
            {"count": result["count"], STATUS: "ok"},
        )

    def get_product_by_customer_id(self, customer_product_id):
        products, next, status = self.get_products(customer_product_id=customer_product_id)
        if not products or len(products) == 0 or status[STATUS] == STATUS_ERROR:
            return None, status
        return products[0], RESULT_OK


class ProductSet(ProductClient):
    def __init__(self, token, endpoint, workspace, product_set_json):
        super().__init__(token, endpoint=endpoint, workspace=workspace, resource_name=None)

        self.id = product_set_json["id"]
        self.name = product_set_json["name"]
        self.year = product_set_json["year"]

    def add_parent(self, parent_set):
        return self.put(PRODUCT_SET_ENDPOINT + self.id, data={"parent": parent_set})


class Product(ProductClient):
    def __init__(self, token, endpoint, workspace, product_json):
        super().__init__(token, endpoint=endpoint, workspace=workspace, resource_name=None)

        self.id = product_json["id"]
        self.name = product_json["name"]
        self.product_collection = product_json["product_collection"]
        self.customer_product_id = product_json["customer_product_id"]
        self.meta_data = product_json.get("meta_data", None)
        self.thumb = product_json.get("thumb", None)
        self.product_set = product_json.get("product_set", None)

    def __str__(self):
        return self.name + ":" + self.id + ":" + str(self.product_collection)

    def remove(self):
        self.remove_product(self.id)

    def update_product(self, **kwargs):
        """Call this as following:

        product.update_product(
            **{
                "name": card.get("name", "") + " " + card.get("year", "") + " #" + card.get("card_number", ""),
                "customer_product_id": card["product"],
                "product_collection": exports[card["Subcategory"]]["id"],
                "meta_data": card
            }
        )
        """
        result = self.patch(PRODUCT_ENDPOINT + self.id, data=kwargs)

    def update_meta(self, new_data):
        result = self.patch(PRODUCT_ENDPOINT + self.id, data={META_DATA: new_data})

    def get_images(self):
        return self.get_all_images(str(self.id))


class ProductImage(ProductClient):
    def __init__(self, token, endpoint, workspace, image_json):
        super().__init__(token, endpoint=endpoint, workspace=workspace, resource_name=None)

        self.id = image_json["id"]
        self.name = image_json["name"]
        self.product = image_json["product"]
        self.meta_data = image_json.get("meta_data", None)
        self.objects = image_json["_objects"]

        self.img = image_json["file"]
        self.img_thumb = image_json["thumb"]

    def __str__(self):
        product = self.product if self.product and isinstance(self.product, str) else ""
        return self.name + ":" + self.id + ":" + product

    def remove(self):
        self.remove_image(self.id)

    def refresh(self):
        newpi = self.get_image(self.id)
        self.name = newpi.name
        self.product = newpi.product
        self.meta_data = newpi.meta_data if newpi.meta_data is not None else {}
        self.objects = newpi.objects

    def update_meta(self, new_data, refresh=False):
        if refresh:
            self.refresh()

        if self.meta_data is None:
            self.meta_data = {}

        self.meta_data.update(new_data)
        self.patch(IMAGE_ENDPOINT + self.id, data={META_DATA: new_data})
