const SKILL_LEVELS = ["Beginner", "Intermediate", "Expert"];

export default function FancySkillSlider({ skill, setSkill }) {
  const currentIndex = SKILL_LEVELS.indexOf(skill);

  const handleChange = (e) => {
    const value = parseInt(e.target.value);
    setSkill(SKILL_LEVELS[value]);
  };

  return (
    <div className=" my-6">
      <div className="relative">
        {/* Slider Input */}
        <input
          type="range"
          min="0"
          max="2"
          step="1"
          value={currentIndex}
          onChange={handleChange}
          className="w-full appearance-none bg-transparent"
        />

        {/* Slider Track + Ticks */}
        <div className="relative mt-2">
          <div className="flex justify-between text-xs text-white/50 px-1">
            {SKILL_LEVELS.map((label, idx) => (
              <span key={idx} className="w-1/2 text-center">
                {label}
              </span>
            ))}
          </div>
        </div>

        {/* Tooltip */}
        {/* <motion.div
          className="absolute top-[-40px] left-0 text-white text-sm font-semibold bg-indigo-600 rounded px-3 py-1 shadow-md"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, x: `${(currentIndex / 2) * 100}%` }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          {skill}
        </motion.div> */}
      </div>

      {/* Custom track styles */}
      <style>{`
        input[type="range"]::-webkit-slider-thumb {
          appearance: none;
          height: 18px;
          width: 18px;
          border-radius: 9999px;
          background: #6366f1;
          cursor: pointer;
          border: 2px solid white;
          margin-top: -6px;
        }
        input[type="range"]::-webkit-slider-runnable-track {
          height: 6px;
          background: #3b3b3b;
          border-radius: 9999px;
        }
      `}</style>
    </div>
  );
}
