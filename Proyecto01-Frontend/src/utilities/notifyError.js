import toast from "react-hot-toast";

export const notifyError = (word) => toast.error(`${word} is not a valid word`, {
    position: "top-right"
});