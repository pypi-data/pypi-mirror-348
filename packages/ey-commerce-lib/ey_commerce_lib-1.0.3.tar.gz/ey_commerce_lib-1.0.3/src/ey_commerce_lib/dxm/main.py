import asyncio

from ey_commerce_lib.dxm.constant.order import DxmOrderRuleType
from ey_commerce_lib.dxm.parser.common import get_page_info
from ey_commerce_lib.dxm.parser.order import list_order_base_by_html, list_order_rule, get_rule_detail, \
    get_order_detail_by_html
from ey_commerce_lib.dxm.parser.purchase import list_purchasing_all
from ey_commerce_lib.dxm.parser.warehouse import list_warehouse_product
from ey_commerce_lib.dxm.schemas.common import Page
from ey_commerce_lib.dxm.schemas.order import DxmOrderSearchForm, DxmJsonResponse, DxmCheckProcessResponse, DxmOrderRule
from ey_commerce_lib.dxm.schemas.warehouse import WarehouseProduct, WarehouseProductQuery, PurchasingAllQuery
from httpx import AsyncClient


class DxmClient:

    def __init__(self, cookies: dict, headers: dict, sem: int = 10):
        self.__cookies = cookies
        self.__headers = headers
        self.__sem = asyncio.Semaphore(sem)
        self.__async_client = AsyncClient(base_url="https://www.dianxiaomi.com", cookies=cookies, headers=headers)

    async def page_order_base_async(self, query: DxmOrderSearchForm):
        """
        条件分页查询订单基础信息
        :param query:
        :return:
        """
        # 查询分页数据
        data = await self.__async_client.post("/package/advancedSearch.htm", data=query.model_dump(by_alias=True))
        # 获取分页信息
        page_info = get_page_info(data.text)
        data = list_order_base_by_html(data.text)
        return {
            **page_info,
            'data': data
        }

    async def list_order_base_async(self, query: DxmOrderSearchForm):
        """
        条件查询订单信息列表
        :return:
        """
        query.page_no = 1
        data = await self.page_order_base_async(query)
        total_page = data['total_page']
        result = data['data']
        for page_number in range(2, total_page + 1):
            query.page_no = page_number
            data = await self.page_order_base_async(query)
            result.extend(data['data'])
        return result

    async def page_order_detail_async(self, query: DxmOrderSearchForm):
        async def set_detail(order_base: dict):
            """
            设置详情
            :param order_base:
            :return:
            """
            order_base['detail'] = await self.package_detail(order_base['package_id'])

        # 获取基本分页数据信息
        page_base_order = await self.page_order_base_async(query)
        # 获取并设置详情信息
        await asyncio.gather(*[
            set_detail(item)
            for item in page_base_order['data']])

        return page_base_order

    async def list_order_detail_async(self, query: DxmOrderSearchForm):
        query.page_no = 1
        data = await self.page_order_detail_async(query)
        total_page = data['total_page']
        result = data['data']
        for page_number in range(2, total_page + 1):
            query.page_no = page_number
            data = await self.page_order_detail_async(query)
            result.extend(data['data'])
        return result

    async def package_detail(self, package_id: str):
        """
        获取包裹的详情数据
        :param package_id:
        :return:
        """
        async with self.__sem:
            package_detail_res = await self.__async_client.post('/package/detail.htm', data={
                'packageId': package_id,
                'history': ''
            })
            return get_order_detail_by_html(package_detail_res.text)

    async def move_process(self, package_id: str) -> DxmJsonResponse:
        """
        申请运单号
        :return:
        """
        async with self.__sem:
            move_processed_json = await self.__async_client.post("/package/moveProcessed.json", data={
                "packageId": package_id
            })
            return move_processed_json.json()

    async def move_allocated(self, package_id: str) -> DxmJsonResponse:
        """
        移入待打单
        :param package_id:
        :return:
        """
        async with self.__sem:
            move_allocated_json = await self.__async_client.post("/package/moveAllocated.json", data={
                "packageId": package_id
            })
            return move_allocated_json.json()

    async def upload_track_num(self, package_id: str, track_num: str, auth_id) -> DxmJsonResponse:
        """
        上传运单号
        :param package_id: package_id
        :param track_num:  运单号
        :param auth_id: 物流方式id
        :return:
        """
        async with self.__sem:
            upload_track_num_json = await self.__async_client.post("/package/uploadTrackNum.json", data={
                "packageId": package_id,
                "trackNum": track_num,
                "authId": auth_id
            })
            return upload_track_num_json.json()

    async def get_warehouse_dict(self):
        """
        获取仓库字典映射
        :return:
        """
        warehouse_info_res = await self.__async_client.get("/dxmWarehoseCon/getWarehoseInfo.json")
        warehouse_info_dict = warehouse_info_res.json()
        result = dict()
        for item in warehouse_info_dict.items():
            result[item[1]['name']] = item[0]
        return result

    async def commit_platform(self, package_id: str):
        """
        虚拟发货
        :param package_id: 包裹id
        :return:
        """
        async with self.__sem:
            commit_platform_res = await self.__async_client.post("/package/commitPlatform.json", data={
                'packageId': package_id
            })
            return commit_platform_res.json()

    async def save_storage_id_for_order(self, package_id: str, storage_id: str):
        """
        订单详情修改订单仓库
        :param package_id:
        :param storage_id:
        :return:
        """
        async with self.__sem:
            save_storage_id_for_order_res = await self.__async_client.post("/package/saveStorageIdForOrder.json", data={
                'packageId': package_id,
                'storageId': storage_id,
                'pids': ''
            })
            return save_storage_id_for_order_res.json()

    async def __refresh_logistics_rule(self, uri: str, all_refresh: int):
        async with self.__sem:
            refresh_logistics_rule_res = await self.__async_client.post(f'/order/{uri}.json', data={
                'shopId': '-1',
                'platform': '',
                'allRefresh': f'{all_refresh}',
            })
            uuid = refresh_logistics_rule_res.json().get('uuid')
            check_process_res = await self.__check_process(uuid)
            # 任务没有完成就一直监测直到任务完成为止
            while int(check_process_res['processMsg']['num']) < int(check_process_res['processMsg']['totalNum']):
                check_process_res = await self.__check_process(uuid)
                await asyncio.sleep(1)
            return check_process_res

    async def refresh_logistics_rule_no_select_logistics_method(self) -> DxmCheckProcessResponse:
        """
        刷新物流规则(待处理中的未选择物流方式的订单)
        :return:
        """
        return await self.__refresh_logistics_rule(uri='refreshLogisticRule', all_refresh=0)

    async def refresh_logistics_rule_all(self) -> DxmCheckProcessResponse:
        """
        刷新物流规则(待处理中的所有订单)
        :return:
        """
        return await self.__refresh_logistics_rule(uri='refreshLogisticRule', all_refresh=1)

    async def refresh_rule_all(self):
        """
        刷新物流规则(待审核中的所有订单)
        :return:
        """
        return await self.__refresh_logistics_rule(uri='refreshRule', all_refresh=1)

    async def refresh_no_select_logistics_method_rule(self):
        """
        刷新物流规则(待审核未选择物流方式的订单)
        :return:
        """
        return await self.__refresh_logistics_rule(uri='refreshRule', all_refresh=0)

    async def __check_process(self, uuid: str) -> DxmCheckProcessResponse:
        """
        检测任务的进度
        :param uuid: 任务id
        :return:
        """
        async with self.__sem:
            check_process_res = await self.__async_client.post("/checkProcess.json", data={
                'uuid': uuid
            })
            return check_process_res.json()

    async def ship_goods(self, package_id: str):
        """
        发货
        :param package_id:
        :return:
        """
        async with self.__sem:
            ship_goods_res = await self.__async_client.post("/package/shipGoods.json", data={
                "packageId": package_id
            })
            return ship_goods_res.json()

    async def batch_ship_goods(self, package_ids: list):
        """
        批量发货
        :param package_ids: package_id列表
        :return:
        """
        async with self.__sem:
            batch_ship_goods_res = await self.__async_client.post("/package/batchShipGoods.json", data={
                "packageIds": ','.join(package_ids)
            })
            return batch_ship_goods_res.json()

    async def list_rule(self, rule_type: DxmOrderRuleType) -> dict:
        """
        获取审单规则列表
        :return:
        """
        async with self.__sem:
            list_rule_res = await self.__async_client.get("/rule/index.htm", params={
                'type': rule_type
            })
            list_rule_html = list_rule_res.text
            data = list_order_rule(list_rule_html)
            # 遍历设置Type
            for item in data:
                item['type'] = rule_type.value
            return data

    async def get_rule_id_by_name(self, rule_name: str, rule_type: DxmOrderRuleType) -> str:
        """
        根据规则名称获取规则
        :param rule_name:
        :param rule_type:
        :return:
        """
        data = await self.list_rule(rule_type)
        for item in data:
            if item['rule_name'] == rule_name:
                return item['rule_id']

    async def rule_detail(self, rule_id: str, rule_type: int):
        """
        获取审单规则详情
        :param rule_id:
        :param rule_type:
        :return:
        """
        async with self.__sem:
            rule_detail_res = await self.__async_client.get("/rule/detail.htm", params={
                'id': rule_id,
                'type': rule_type,
                'isCopy': '0'
            })
            rule_detail_html = rule_detail_res.text
            return get_rule_detail(rule_detail_html)

    async def update_rule(self, dxm_rule_order: DxmOrderRule):
        """
        更新审单规则
        :param dxm_rule_order:
        :return:
        """
        data = dxm_rule_order.to_update_rule_data()
        async with self.__sem:
            update_rule_res = await self.__async_client.post("/rule/update.json", content=data)
            return update_rule_res.json()

    async def edit_rule_state(self, rule_id: str, state: int):
        """
        编辑规则状态
        :param rule_id: 规则id
        :param state: 1启用 0禁用
        :return:
        """
        async with self.__sem:
            edit_rule_state_res = await self.__async_client.post("/rule/editRuleState.json", data={
                'id': rule_id,
                'state': state
            })
            return edit_rule_state_res.json()

    async def enable_rule(self, rule_id: str):
        """
        启用规则
        :param rule_id:
        :return:
        """
        return await self.edit_rule_state(rule_id, 1)

    async def disable_rule(self, rule_id: str):
        """
        禁用规则
        :param rule_id:
        :return:
        """
        return await self.edit_rule_state(rule_id, 0)

    async def batch_enable_rule(self, rule_id_list: list):
        """
        批量启用规则
        :param rule_id_list:
        :return:
        """
        await asyncio.gather(*[self.enable_rule(rule_id) for rule_id in rule_id_list])

    async def batch_disable_rule(self, rule_id_list: list):
        """
        批量禁用规则
        :param rule_id_list:
        :return:
        """
        await asyncio.gather(*[self.disable_rule(rule_id) for rule_id in rule_id_list])

    async def page_warehouse_product(self, query: WarehouseProductQuery) -> Page[WarehouseProduct]:
        """
        分页查询仓库商品
        :param query: 查询条件
        :return:
        """
        async with self.__sem:
            page_warehouse_product_res = await self.__async_client.post("/warehouseProduct/pageList.htm",
                                                                        data=query.model_dump(by_alias=True))
            return Page(data=list_warehouse_product(page_warehouse_product_res.text),
                        **get_page_info(page_warehouse_product_res.text))

    async def list_warehouse_product(self, query: WarehouseProductQuery) -> list[WarehouseProduct]:
        """
        查询仓库商品
        :param query:
        :return:
        """
        data = await self.page_warehouse_product(query)
        total_page = data.total_page
        result = data.data
        for page_number in range(2, total_page + 1):
            query.page_no = page_number
            data = await self.page_warehouse_product(query)
            result.extend(data.data)
        return result

    async def page_purchasing_all(self, query: PurchasingAllQuery):
        """
        分页查询采购单
        :return:
        """
        async with self.__sem:
            page_purchasing_all_pageList_res = await self.__async_client.post(
                "/dxmPurchasingNote/purchasingAllPageList.htm",
                data=query.model_dump(by_alias=True))
            list_purchasing_all(page_purchasing_all_pageList_res.text)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__async_client.aclose()
