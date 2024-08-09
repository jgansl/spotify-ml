migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  collection.deleteRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  collection.deleteRule = null

  return dao.saveCollection(collection)
})
