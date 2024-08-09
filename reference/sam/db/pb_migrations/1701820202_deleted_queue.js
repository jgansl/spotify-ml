migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "8g478vgl2qaz0kf",
    "created": "2023-12-05 02:11:04.455Z",
    "updated": "2023-12-05 02:21:52.069Z",
    "name": "queue",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "hh12ng37",
        "name": "spotify_id",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "ejqshd8a",
        "name": "sid",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "pup57hfx",
        "name": "release_date",
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
    "deleteRule": "",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
})
