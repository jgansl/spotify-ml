migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.updateRule = ""

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  collection.updateRule = null

  return dao.saveCollection(collection)
})
