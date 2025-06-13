import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

const UserDashboard = () => {
  const [content, setContent] = useState("");
  const [senderName, setSenderName] = useState("");
  const [platform, setPlatform] = useState("Instagram");
  const [otherPlatform, setOtherPlatform] = useState("");
  const [location, setLocation] = useState("");
  const [analysisResults, setAnalysisResults] = useState<Record<string, number> | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const analyzeContent = async () => {
    if (!content.trim()) return;

    setIsAnalyzing(true);

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: content,
          sender: senderName,
          platform: platform === "Other" ? otherPlatform : platform,
          location: location,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch analysis results");
      }

      const data = await response.json();

      const filtered = Object.fromEntries(
        Object.entries(data.analysis).filter(([, score]) => score >= 0.7)
      );

      setAnalysisResults(filtered);
    } catch (error) {
      console.error("Error analyzing content:", error);
      alert("Error analyzing content. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">User Threat Report</h1>

      <div className="space-y-4">
        <div>
          <Label>Content (Message or Comment)</Label>
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter the suspicious message or comment..."
          />
        </div>

        <div>
          <Label>Sender Name</Label>
          <Input
            value={senderName}
            onChange={(e) => setSenderName(e.target.value)}
            placeholder="Enter the sender's name"
          />
        </div>

        <div>
          <Label>Platform</Label>
          <select
            className="w-full border rounded p-2"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
          >
            <option value="Instagram">Instagram</option>
            <option value="YouTube">YouTube</option>
            <option value="Reddit">Reddit</option>
            <option value="Other">Other</option>
          </select>
        </div>

        {platform === "Other" && (
          <div>
            <Label>Specify Platform</Label>
            <Input
              value={otherPlatform}
              onChange={(e) => setOtherPlatform(e.target.value)}
              placeholder="Enter the platform name"
            />
          </div>
        )}

        <div>
          <Label>Location (optional)</Label>
          <Input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter location if known"
          />
        </div>

        <Button onClick={analyzeContent} disabled={isAnalyzing}>
          {isAnalyzing ? "Analyzing..." : "Analyze"}
        </Button>
      </div>

      {analysisResults && (
        <div className="mt-6 space-y-2">
          <h2 className="text-xl font-semibold">Analysis Results (Threshold ≥ 0.7)</h2>
          {Object.entries(analysisResults).map(([label, score]) => (
            <div key={label} className="flex items-center justify-between bg-gray-100 p-2 rounded">
              <span className="capitalize font-medium">{label}</span>
              <span>{(score * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UserDashboard;
