// Put `add.wasm` in `public/wasm/` folder
// (or any other static folder)
WebAssembly.instantiateStreaming(
   // Fetch the file and stream into the WebAssembly runtime
   fetch('/wasm/add.wasm')
 ).then((result) => result.instance.exports.add(1, 1)) // = 2