import { Dialog, Transition } from "@headlessui/react"
import { Fragment } from "react"
import { Input } from "./Input"

export const Modal = ({ isOpen, setIsOpen, formData, handleOnChange, handleSubmit }) => {
  const fields = Object.keys(formData);

  const closeModal = () => {
    handleSubmit();
    setIsOpen(false)
  }

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={closeModal}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="text-xl leading-6 text-gray-900 font-bold mb-4"
                >
                  Enter the required values
                </Dialog.Title>

                {
                  fields.map(field => (
                    <Input
                      type={formData[field].type}
                      placeholder={formData[field].placeholder}
                      handleOnChange={(value) => handleOnChange(field, value.target.value)}
                    />
                  ))
                }

                <div className="mt-4">
                  <button
                    type="button"
                    className="inline-flex justify-center items-center rounded-md border border-transparent bg-cyan-100 px-4 py-2 font-medium text-cyan-900
                       hover:bg-cyan-200 transition-colors gap-2"
                    onClick={closeModal}
                  >
                    Send
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 m-0">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
                    </svg>
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
}
