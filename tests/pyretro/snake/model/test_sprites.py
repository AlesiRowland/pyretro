# """
#
# """
# import pytest
# from pytest_cases import fixture, fixture_ref, parametrize
#
# from snake.model.sprites.rect import SnakeRect
# from snake.model.sprites.types import Snake, SnakeFood
# from snake.model.structs import Point
#
#
# @fixture
# def snake_head() -> SnakeRect:
#     return SnakeRect(50, 50, 20, 20)
#
#
# @fixture
# def snake_tail() -> tuple[SnakeRect, ...]:
#     return (
#         SnakeRect(50, 70, 20, 20),
#         SnakeRect(50, 90, 20, 20),
#     )
#
#
# @pytest.mark.unit
# class TestSnakeFood:
#     @fixture
#     def snake_food(self) -> SnakeFood:
#         return SnakeFood(SnakeRect(20, 20, 20, 20))
#
#     def test_len(self, snake_food):
#         assert len(snake_food) == 1
#
#
# @pytest.mark.unit
# class TestSnake:
#
#     @fixture
#     def collides_snake(self, snake_head):
#         return Snake(
#             snake_head,
#             (
#                 SnakeRect(50, 90, 20, 20),
#                 SnakeRect(50, 70, 20, 20),
#                 SnakeRect(50, 50, 20, 20)
#             )
#         )
#
#     @fixture
#     def head_only_snake(self, snake_head):
#         return Snake(snake_head)
#
#     @fixture
#     def prebuilt_snake(self, snake_head, snake_tail):
#         return Snake(snake_head, snake_tail)
#
#     def test_len(self, prebuilt_snake):
#         assert len(prebuilt_snake) == 3
#
#     def test_rects(self, prebuilt_snake):
#         assert prebuilt_snake.rects == [
#             SnakeRect(50, 50, 20, 20),
#             SnakeRect(50, 70, 20, 20),
#             SnakeRect(50, 90, 20, 20),
#         ]
#
#     @parametrize("snake",
#                  [fixture_ref("prebuilt_snake"), fixture_ref("head_only_snake")]
#                  )
#     def test_head(self, snake, snake_head):
#         assert snake.head == snake_head
#
#     def test_tail(self, prebuilt_snake):
#         assert prebuilt_snake.tail == [
#             SnakeRect(50, 70, 20, 20),
#             SnakeRect(50, 90, 20, 20),
#         ]
#
#     def test_empty_tail(self, head_only_snake):
#         assert head_only_snake.tail == []
#
#     def test_move(self, prebuilt_snake):
#         prebuilt_snake.move(Point(0, 20))
#         expected = Snake(
#
#             SnakeRect(50, 70, 20, 20),
#             (
#                 SnakeRect(50, 50, 20, 20),
#                 SnakeRect(50, 70, 20, 20),
#             )
#
#         )
#         assert prebuilt_snake == expected
#
#     def test_move_and_grow(self, prebuilt_snake):
#         prebuilt_snake.move(Point(0, 20), grow=True)
#         expected = Snake(
#             SnakeRect(50, 70, 20, 20),
#             (
#                 SnakeRect(50, 50, 20, 20),
#                 SnakeRect(50, 70, 20, 20),
#                 SnakeRect(50, 90, 20, 20),
#             )
#         )
#         assert prebuilt_snake == expected
#
#     def test_collides_true(self, collides_snake):
#         assert collides_snake.collides_with_self() is True
#
#     @parametrize("snake", [fixture_ref("head_only_snake"), fixture_ref("prebuilt_snake")])
#     def test_collides_false(self, snake):
#         assert snake.collides_with_self() is False
