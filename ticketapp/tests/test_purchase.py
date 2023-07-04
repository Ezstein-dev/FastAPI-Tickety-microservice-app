# import unittest
# from fastapi.testclient import TestClient
# from ..api.purchase import app

# client = TestClient(app)

# class TestPurchase(unittest.TestCase):

#     def test_create_order(self):
#         # Test creating a new order
#         response = client.post(
#             "/orders/",
#             json={"id": 1, "quantity": 2},
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_create_order_with_invalid_ticket(self):
#         # Test creating a new order with an invalid ticket ID
#         response = client.post(
#             "/orders/",
#             json={"id": 999, "quantity": 2},
#         )
#         self.assertEqual(response.status_code, 404)

#     def test_create_order_with_insufficient_quantity(self):
#         # Test creating a new order with insufficient ticket quantity
#         response = client.post(
#             "/orders/",
#             json={"id": 1, "quantity": 999},
#         )
#         self.assertEqual(response.status_code, 400)

#     def test_get_order(self):
#         # Test getting an existing order
#         response = client.get(
#             "/orders/1",
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_get_order_with_invalid_id(self):
#         # Test getting an order with an invalid ID
#         response = client.get(
#             "/orders/999",
#         )
#         self.assertEqual(response.status_code, 404)
