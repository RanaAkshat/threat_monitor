import { useQuery } from "@tanstack/react-query";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const useThreats = () => {
  return useQuery({
    queryKey: ["threats"],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/threats`);
      if (!response.ok) {
        throw new Error("Failed to fetch threats");
      }
      const data = await response.json();
      return data.tweets;
    },
  });
};
