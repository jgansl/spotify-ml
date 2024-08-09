migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.createRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.createRule = null

  return dao.saveCollection(collection)
})
