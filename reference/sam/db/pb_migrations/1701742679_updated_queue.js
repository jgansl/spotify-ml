migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  collection.deleteRule = null

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
})
