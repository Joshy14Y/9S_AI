import toast from "react-hot-toast";

export const notifyResult = (result) => toast.success(`Result: ${result}`, {
  duration: 7000,
  style: {
    border: '1px solid #0891b2',
    padding: '16px',
    color: '#0891b2',
  },
  iconTheme: {
    primary: '#0891b2',
    secondary: '#FFFAEE',
  },
});