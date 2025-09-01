// components/PostCard.js
export default function PostCard({ title, sentiment }) {
  let color = "black";
  if (sentiment === "positive") color = "green";
  else if (sentiment === "negative") color = "red";

  return (
    <div className={`p-4 rounded shadow border-l-4 border-${color}-500 bg-black`}>
      <h2 className="font-bold text-white" >{title}</h2>
      <p className={`text-${color}-600`}>Sentiment: {sentiment}</p>
    </div>
  );
}
