import React from "react"; import { motion } from "framer-motion"; import { Helmet } from "react-helmet";

const fadeInUp = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } };

export default function Portfolio() { return ( <>  <Helmet> <title>Sasi Manchina | Data Engineer Portfolio</title> <meta name="description" content="Portfolio of Sasi Manchina – Data Engineer, AI/ML Developer, and Cloud Specialist." /> <meta property="og:title" content="Sasi Manchina Portfolio" /> <meta property="og:description" content="Check out the projects and experience of Sasi Manchina in Data Engineering and AI." /> <meta property="og:type" content="website" /> <meta property="og:url" content="https://sasimanchina7.github.io/Manchina.dev" /> <meta property="og:image" content="https://yourdomain.com/preview.png" /> <link rel="icon" href="/favicon.ico" type="image/x-icon" /> <meta name="theme-color" content="#1f2937" /> </Helmet>

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

```
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

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Professional Summary</h2>
  <ul className="list-disc pl-5 text-sm space-y-1">
    <li>~5 years of combined AI experience with Python, TensorFlow, and multi-platform data pipelines.</li>
    <li>Hands-on with Matplotlib, Seaborn, Power BI, Tableau, SAS; strong data visualization and suppression skills.</li>
    <li>Experience in hypothesis testing, statistical modeling, ML algorithms (Regression, Clustering, LSTM, etc.), and cloud data analytics.</li>
    <li>Big Data: MySQL, BigQuery, Hadoop, Spark; skilled in writing efficient SQL queries and data integration.</li>
    <li>Experienced in DevOps workflows (CI/CD), VS Code, Java 11, OOP, concurrency, XCode for app development.</li>
    <li>Strong communicator and independent problem solver with deep learning agility and cross-functional collaboration skills.</li>
  </ul>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.1 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Skills</h2>
  <p className="text-sm leading-6">
    <strong>Languages:</strong> Python, Java, SQL, Swift, JavaScript, HTML, CSS, XML, R, .NET<br/>
    <strong>Frameworks & Tools:</strong> TensorFlow, Tableau, Power BI, SAS, SMOTE, Angular 8, React, SPSS<br/>
    <strong>Big Data:</strong> BigQuery, GCP, AWS, Azure, CI/CD, Anaconda, NLP, Jupyter<br/>
    <strong>Platforms:</strong> Salesforce, Oracle, Automation Anywhere, Kubernetes, Virtual Studio, Collab, ServiceNow
  </p>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.2 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Experience</h2>
  <p className="text-sm">
    <strong>Amazon MME2 FC, UK – Peer Trainer & POC</strong> (Oct 2022 – Jan 2025)<br/>
    Led cross-functional problem solve initiatives at Amazon FC. Owned dwell resolution, internal system navigation (APT, Pandash, POPS), and new hire training. Authenticated inventory issue resolutions and facilitated continuous improvement with ops leadership.
  </p>
  <p className="text-sm mt-3">
    <strong>ModelN Software Pvt Ltd – Associate Consultant</strong> (May 2020 – Sep 2022)<br/>
    Delivered integration frameworks for MDM and payment system pipelines across four enterprise-grade healthcare/life sciences projects. Wrote SQL, Python, and API scripts and deployed scalable BI dashboards.
  </p>
  <p className="text-sm mt-3">
    <strong>Kaashiv Infotech – Academic Intern</strong> (Jun 2019 – May 2020)<br/>
    Developed ML stock prediction models with Google AutoML and LSTM; explored digital marketing and data science.
  </p>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.3 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Projects</h2>
  <p className="text-sm">
    <strong>Stock Purchase Web Extension (Teesside University, 2022–2024)</strong><br/>
    Built an intelligent recommendation system for stock buys using LSTM, regression, SMOTE, and Python. Developed a Swift-based frontend and Angular dashboard. Integrated MySQL/Oracle queries and BI visualizations. Hosted extension with customizable ticker inputs.
  </p>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.4 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Education</h2>
  <ul className="list-disc pl-5 text-sm">
    <li>MSc Artificial Intelligence with Data Analytics – Teesside University, UK</li>
    <li>BTech Computer Science (Data Science) – KL University, India</li>
    <li>Higher Secondary – Sasi Junior College, India</li>
    <li>High School – Sasi Educational Institutes, India</li>
  </ul>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.5 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Certifications</h2>
  <ul className="list-disc pl-5 text-sm">
    <li>Salesforce Certified Application Architect</li>
    <li>Oracle Certified Associate, Java SE 8 Programmer</li>
    <li>Google Cloud Certified Professional Cloud Architect</li>
    <li>Automation Anywhere Advanced RPA Professional</li>
    <li>Big Data Hadoop & Spark Developer</li>
    <li>Google Kubernetes Engine Certified</li>
    <li>ServiceNow Certified Tool-Based Training</li>
    <li>Machine Learning Advanced Professional Certification</li>
  </ul>
</motion.section>

<motion.section variants={fadeInUp} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.6, delay: 0.6 }}>
  <h2 className="text-2xl font-semibold border-b pb-2 mb-4 text-gray-900 dark:text-white">Publications</h2>
  <p className="text-sm">
    <strong>Prediction of Fake Tweets Using ML – ResearchGate, May 2021</strong><br/>
    Researched fake news detection using NLP and supervised learning. Targeted Twitter dataset classification with feature extraction and model performance comparison.
  </p>
</motion.section>
```

  </main>

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9553234023"></script>

  <script>
    {`
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-9553234023');
    `}
  </script>

\</> ); }
