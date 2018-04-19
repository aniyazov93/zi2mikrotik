# zi2mikrotik
Приложение, которое парсит выгрузку роскомнадзора. Даёт выгрузку адресов и подсетей, считает общее количество заблокированных адресов.
Есть возможность выгрузки в формате mikrotik для использования со скриптом. 

В качестве источника данных используется репозиторий https://github.com/zapret-info/z-i

Выгрузка обновляется в фоновом режиме автоматически каждые 600 секунд.

# endpoints

**Список заблокированных узлов и сетей**
----
    Вернёт список в формате json  

* **URL**
    /info 
    
* **Method:**
    GET
    
* **Parameters:**
    
     **Optional:**     
    `networks=true`   
    `addresses=true`
    
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

**Mikrotik формат**
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

  
**Общее число заблокированных узлов**
----
    Вернёт общее число заблокированных IP адресов. По умолчанию используется формат json

* **URL**
    /banned_count 
    
* **Method:**
    GET
    
* **Parameters:**

    **optional:**     
    `raw=[bool]` - Отдавать ли только число, без всякого форматирования
       
    
* **Success responce:**
    * **Code:** 200 <br />
        **Content:** 
        `{
  "total_banned": 16476112
}`