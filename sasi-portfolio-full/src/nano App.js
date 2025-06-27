import React from "react"; import { motion } from "framer-motion"; import { Helmet } from "react-helmet";

const fadeInUp = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } };

export default function Portfolio() { return ( <>  Sasi Manchina | Data Engineer Portfolio        &#x20;

```
  <main className="max-w-4xl mx-auto px-6 py-10 space-y-14 text-gray-800 dark:text-gray-200 dark:bg-gray-900">
    <div className="flex justify-end">
      <button
        onClick={() => {
          document.documentElement.classList.toggle("dark");
          localStorage.theme = document.documentElement.classList.contains("dark") ? "dark" : "light";
        }}
        className="text-sm px-4 py-2 border rounded-full shadow-sm bg-white dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600"
      >
        🌓 Toggle Theme
      </button>
    </div>

    <motion.header 
      className="text-center space-y-2"
      variants={fadeInUp} 
      initial="hidden" 
      animate="visible" 
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-4xl font-bold tracking-tight">Sasi Manchina</h1>
      <p className="text-lg text-gray-600 dark:text-gray-400">Data Engineer | AI/ML Developer | Cloud Native Specialist</p>
      <p className="text-sm text-gray-500 dark:text-gray-400">Bangalore, India • sasimanchina@gmail.com</p>
      <a
        href="https://linkedin.com/in/manchina-bhavani-krishna-veni-62b6b0279"
        className="inline-block text-blue-500 hover:text-blue-700 underline text-sm font-medium"
        target="_blank"
        rel="noopener noreferrer"
      >LinkedIn Profile</a>
    </motion.header>

    {["Professional Summary", "Skills", "Experience", "Projects", "Education", "Contact"].map((title, index) => (
      <motion.section
        key={title}
        variants={fadeInUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.6, delay: index * 0.1 }}
      >
        <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">{title}</h2>
        <p className="text-sm text-gray-600 dark:text-gray-300 italic">Section content goes here...</p>
      </motion.section>
    ))}
  </main>

  {/* Google Analytics (Optional: Replace G-XXXXXX with your ID) */}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
  <script>
    {`
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXX');
    `}
  </script>
</>
```

); }
