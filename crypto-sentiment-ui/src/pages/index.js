import { useEffect, useState } from "react";
import PostCard from "@/components/PostCard"; // using the @ alias

export default function Home() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch("http://localhost:8000/api/sentiment");
      const data = await res.json();
      setPosts(data);
    }
    fetchPosts();
  }, []);

  return (
    <div className="p-6 bg-gray-300 min-h-screen">
      <h1 className="text-3xl font-bold text-black  mb-3 ">Crypto Sentiment Tracker</h1>
      <div className="grid gap-4">
        {posts.map((post, index) => (
          <PostCard
            key={index}
            title={post.title}
            sentiment={post.sentiment}
          />
        ))}
      </div>
    </div>
  );
}
