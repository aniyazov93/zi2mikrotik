# zi2mikrotik
Приложение, которое генерирует списки маршрутов до заблокированных роскомнадзором адресов и сетей.
Есть возможность выгрузки в формате mikrotik для использования со скриптом. 

В качестве источника данных используется репозиторий https://github.com/zapret-info/z-i

Выгрузка обновляется в фоновом режиме автоматически каждые 120 секунд. На время обновления все эндпоинты отдают 204 код с путым телом.

# endpoints

**Список заблокированных узлов и сетей**
----
    Вернёт список в формате json  

* **URL**
    /info 
    
* **Method:**
    GET
    
* **Parameters:**
    None
    
* **Success responce:**
    * **Code:** 200 <br />
        **Content:** `{
  "addresses": [
    "<address 1>", 
    ...
    "<address n>"
  ], 
  "networks": [
    "<net 1>", 
    ... 
    "<net n>"
  ]
}`
* **Error Response:**

  * **Code:** 204 <br />

**Mikrotik format**
----
    Вернёт список в формате команд RouterOS.

* **URL**
    /mikrotik 
    
* **Method:**
    GET
    
* **Parameters:**

    **Required:**     
    `gw=[string]` - Шлюз или название интерфейса, куда направлять трафик
    
    **Required(at least one of):**     
    `networks=true` - Добавлять ли подсети в правила
    `addresses=true` - Добавлять ли IP адреса в правила
       
    
* **Success responce:**
    * **Code:** 200 <br />
        **Content:** 
        `/ip routes add dst-address=<address or network> gateway=<gateway> comment=RTKbanned`


* **Error Response:**

  * **Code:** 204 <br />