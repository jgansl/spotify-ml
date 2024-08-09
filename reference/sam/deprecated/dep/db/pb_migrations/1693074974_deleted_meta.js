migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("6byes93c5bu9czn");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "6byes93c5bu9czn",
    "created": "2023-04-15 20:54:01.226Z",
    "updated": "2023-04-15 20:54:44.278Z",
    "name": "meta",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "kjsw8ur1",
        "name": "lastUnsortedToSaved",
        "type": "text",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      }
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
})
