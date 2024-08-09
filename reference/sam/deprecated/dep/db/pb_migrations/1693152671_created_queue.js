migrate((db) => {
  const collection = new Collection({
    "id": "bszklb23jxrrv02",
    "created": "2023-08-27 16:11:11.212Z",
    "updated": "2023-08-27 16:11:11.212Z",
    "name": "queue",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "1yyrsquo",
        "name": "sid",
        "type": "text",
        "required": false,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "jgtswhzk",
        "name": "artist",
        "type": "text",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "qnueeiyg",
        "name": "genre",
        "type": "text",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "oakrzj8p",
        "name": "name",
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
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("bszklb23jxrrv02");

  return dao.deleteCollection(collection);
})
