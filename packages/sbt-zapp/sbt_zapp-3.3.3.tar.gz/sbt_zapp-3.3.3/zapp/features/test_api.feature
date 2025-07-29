
@petstore @smoke @api
Feature: Тестирование Petstore API с использованием стандартных шагов
#запускать только тмс 1
  @TMS-001 @critical
  Scenario: Полный жизненный цикл питомца
    When Я выполнил POST запрос к "https://petstore.swagger.io/v2/pet" c аргументами {"headers":{"Content-Type":"application/json"}} и JSON из "pet_post.json"
    Then Я убедился что с сервера пришел ответ 200
    And Я убедился что ответ соответствует схеме из файла "pet_schema.json"
    And Я сохранил значение поля "id" из ответа с сервера в переменную "pet_id"

    When Я выполнил GET запрос к "https://petstore.swagger.io/v2/pet/" c аргументами {"link_appendix_var": "pet_id"}
    Then Я убедился что с сервера пришел ответ 200
    And Я убедился что в ответе с сервера поле "name" имеет значение "Rex"

    When Я выполнил POST запрос к "https://petstore.swagger.io/v2/pet/{{pet_id}}" c аргументами {"headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": "name=Max&status=sold"}
    Then Я убедился что с сервера пришел ответ 200

    When Я выполнил GET запрос к "https://petstore.swagger.io/v2/pet/{{pet_id}}"
    Then Я убедился что в ответе с сервера поле "name" имеет значение "Max"
    And Я убедился что в ответе с сервера поле "status" имеет значение "sold"

  @TMS-002 @negative
  Scenario: Проверка обработки ошибок
    When Я выполнил GET запрос к "https://petstore.swagger.io/v2/pet/9999999"
    Then Я убедился что с сервера пришел ответ 404
    And Я убедился что в ответе с сервера поле "message" имеет значение "Pet not found"

  @TMS-003 @order
  Scenario: Создание и проверка заказа
    When Я выполнил POST запрос к "https://petstore.swagger.io/v2/store/order" c аргументами { "json": { "petId": 12345, "quantity": 1, "shipDate": "2024-01-01T00:00:00.000Z", "status": "placed", "complete": true } }
    Then Я убедился что с сервера пришел ответ 200
    And Я убедился что ответ соответствует схеме из файла "order_schema.json"
    And Я сохранил значение поля "id" из ответа с сервера в переменную "order_id"

    When Я выполнил GET запрос к "https://petstore.swagger.io/v2/store/order/{{order_id}}"
    Then Я убедился что с сервера пришел ответ 200
    And Я убедился что в ответе с сервера поле "status" имеет значение "placed"