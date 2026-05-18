import { useEffect, useState } from "react";
import UserAccountViewModal from "../../../components/userAdmin/UserAccountViewModal";
import { viewUserAccount } from "../../../api/userAccountApi";

function viewUserAccountPage({ accountId, onClose }) {
  const [account, setAccount] = useState(null);
  const [error, setError] = useState("");

  async function onClick(accountID) {
    try {
      const result = await viewUserAccount(accountID);
      setAccount(result);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    onClick(accountId);
  }, [accountId]);

  if (error) return <p className="error-message">{error}</p>;
  if (!account) return null;

  return <UserAccountViewModal account={account} onClose={onClose} />;
}

export default viewUserAccountPage;
