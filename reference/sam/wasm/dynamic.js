import dynamic from 'next/dynamic'

export interface AddModuleExports {
  add(a: Number, b: Number): Number
}

interface RustComponentProps {
  number: Number
}

const RustComponent = dynamic({
  loader: async () => {
    // Import the wasm module
    // @ts-ignore
    const exports = (await import('../add.wasm')) as AddModuleExports
    const { add } = exports

    // Return a React component that calls the add_one method on the wasm module
    return ({ a, b }: RustComponentProps) => (
      <div>
        <>{add(a, b)}</>
      </div>
    )
  },
})