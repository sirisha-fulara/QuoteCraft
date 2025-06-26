import React, { useState } from "react";
import { HeroGeometric } from "./components/HeroSection";
import FancySkillSlider from "./components/FancySkillSlider";

function App() {
  const [description, setDescription] = useState("");
  const [skill, setSkill] = useState("Intermediate");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setPrediction(null);
    setError(null);

    try {
      const response = await fetch("https://quotecraft-1.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description, skill }),
      });

      const data = await response.json();
      if (data.error) setError(data.error);
      else setPrediction(data.prediction);
    } catch (err) {
      setError("Something went wrong: " + err.message);
    }
  };

  return (
    <div>
      <HeroGeometric />
      <div style={{
        height:600,
        justifyContent:"center",
        alignContent:"center",
        background:"radial-gradient(circle,rgba(54, 75, 89, 1) 0%, rgba(112, 74, 74, 1) 35%, rgba(94, 58, 89, 1) 100%)"
      }}>
        <div
          style={{
            maxWidth: 600,
            margin: "auto",
            padding: 20,
            background: "#111",
            marginTop: "20px",
            borderRadius: "8px",
          }}
        >
          <form onSubmit={handleSubmit}>
            <label className="text-sm font-medium text-white block mb-2">
              Project Description:
            </label>
            <textarea
              placeholder="Enter job description..."
              className="block p-2.5 w-full text-sm text-white bg-gray-800 rounded-lg border border-gray-600 placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              style={{ fontSize: 16, marginBottom: 12 }}
            />

            <label className="text-sm font-medium text-white block mt-4 mb-2">
              Skill Level:
            </label>
            <div className="bg-[#111] text-white">
              <FancySkillSlider skill={skill} setSkill={setSkill} />
            </div>

            <button
              type="submit"
              className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded"
            >
              Predict Price
            </button>
          </form>

          {prediction && (
            <h2 className="mt-4 text-xl text-green-400">💰 {prediction}</h2>
          )}
          {error && (
            <p className="mt-4 text-red-400 font-medium">{error}</p>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
