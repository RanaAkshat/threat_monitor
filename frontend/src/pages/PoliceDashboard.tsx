import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

type Tweet = {
  id: string | number;
  user: string;
  text: string;
  category: string;
  created_at?: string;
};

const PoliceDashboard = () => {
  const [data, setData] = useState<Tweet[]>([]);
  const [filteredData, setFilteredData] = useState<Tweet[]>([]);
  const [search, setSearch] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const tweetsPerPage = 8;
  const [sortKey, setSortKey] = useState<keyof Tweet>("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    handleSearch(search);
  }, [data, search]);

  const fetchData = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/threats");
      setData(res.data.tweets);
    } catch (err) {
      console.error("❌ Error fetching data:", err);
    }
  };

  const handleSearch = (query: string) => {
    const filtered = data.filter((tweet) =>
      tweet.text.toLowerCase().includes(query.toLowerCase()) ||
      tweet.user.toLowerCase().includes(query.toLowerCase()) ||
      tweet.category.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredData(filtered);
    setCurrentPage(1);
  };

  const sortData = (key: keyof Tweet) => {
    const order = key === sortKey && sortOrder === "asc" ? "desc" : "asc";
    const sorted = [...filteredData].sort((a, b) => {
      const valA = a[key] || "";
      const valB = b[key] || "";
      return order === "asc"
        ? valA > valB ? 1 : -1
        : valA < valB ? 1 : -1;
    });
    setSortKey(key);
    setSortOrder(order);
    setFilteredData(sorted);
  };

  const indexOfLast = currentPage * tweetsPerPage;
  const indexOfFirst = indexOfLast - tweetsPerPage;
  const currentTweets = filteredData.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(filteredData.length / tweetsPerPage);

  const categories = Array.from(new Set(data.map((t) => t.category)));
  const categoryCounts = categories.map((cat) => data.filter((t) => t.category === cat).length);

  const chartData = {
    labels: categories,
    datasets: [
      {
        label: "Threat Category Distribution",
        data: categoryCounts,
        backgroundColor: "#1E40AF",
      },
    ],
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">🚓 Police Threat Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {categories.map((cat, i) => (
          <Card key={cat}>
            <CardHeader>
              <CardTitle>{cat}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">{categoryCounts[i]}</p>
              <p className="text-sm text-gray-500">Flagged Tweets</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mb-4">
        <Input
          placeholder="Search user, text or category..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="mb-6">
        <Bar data={chartData} />
      </div>

      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead onClick={() => sortData("user")} className="cursor-pointer">User</TableHead>
              <TableHead onClick={() => sortData("text")} className="cursor-pointer">Text</TableHead>
              <TableHead onClick={() => sortData("category")} className="cursor-pointer">Category</TableHead>
              <TableHead onClick={() => sortData("created_at")} className="cursor-pointer">Created At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentTweets.map((tweet, i) => (
              <TableRow key={i}>
                <TableCell>{tweet.user}</TableCell>
                <TableCell>{tweet.text.slice(0, 80)}...</TableCell>
                <TableCell>{tweet.category}</TableCell>
                <TableCell>{tweet.created_at || "N/A"}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="flex justify-between mt-6">
        <Button disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Previous</Button>
        <p>Page {currentPage} of {totalPages}</p>
        <Button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</Button>
      </div>
    </div>
  );
};

export default PoliceDashboard;
