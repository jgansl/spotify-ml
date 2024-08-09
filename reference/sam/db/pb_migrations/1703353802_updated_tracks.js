migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  collection.listRule = null

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  collection.listRule = ""

  return dao.saveCollection(collection)
})
