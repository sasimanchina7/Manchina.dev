import React from "react";

export default function Portfolio() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-10 space-y-10 text-gray-800">
      <header className="text-center">
        <h1 className="text-4xl font-bold">Sasi Manchina</h1>
        <p className="text-lg mt-2">Junior Sports Analyst | Data-Driven Insights | Performance Analytics</p>
        <p className="text-sm text-gray-500 mt-1">Bangalore, India • sasimanchina@gmail.com</p>
        <a
          href="https://linkedin.com/in/manchina-bhavani-krishna-veni-62b6b0279"
          className="text-blue-600 underline text-sm"
          target="_blank"
        >LinkedIn Profile</a>
      </header>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Professional Summary</h2>
        <p className="mt-2">
          Results-oriented Senior Data Engineer with 5+ years of experience in designing large-scale ETL pipelines, developing AI/ML-driven data products, and delivering scalable cloud-based solutions using GCP, AWS, and Azure. Adept at using Python, Spark, Hadoop, and Java for distributed data processing. Proven expertise in working with big data ecosystems, real-time analytics, and cross-functional team leadership.
        </p>
      </section>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Skills</h2>
        <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
          <div><strong>Languages:</strong> Python, Java, SQL, Scala, Bash</div>
          <div><strong>Cloud Platforms:</strong> GCP, AWS, Azure</div>
          <div><strong>Big Data:</strong> Hadoop, Spark, Hive, Kafka, BigQuery</div>
          <div><strong>ETL Tools:</strong> Apache Airflow, Informatica, Dataflow, Talend</div>
          <div><strong>ML/AI:</strong> TensorFlow, Scikit-learn, LSTM, NLP, Reinforcement Learning</div>
          <div><strong>Visualization:</strong> Power BI, Tableau, Looker, Matplotlib, Seaborn</div>
          <div><strong>Databases:</strong> BigQuery, Oracle, MySQL, MongoDB, PostgreSQL</div>
          <div><strong>Other Tools:</strong> Git, Docker, REST APIs, CI/CD, Xcode, Linux</div>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Experience</h2>
        <div className="mt-4">
          <h3 className="font-bold">Amazon MME2 FC, UK</h3>
          <p className="text-sm text-gray-600">Data Operations Lead & Peer Trainer (2022–2025)</p>
          <ul className="list-disc pl-5 text-sm mt-1 space-y-1">
            <li>Developed and maintained scalable operational dashboards using internal tools (APT, Pandash, POPS).</li>
            <li>Led real-time troubleshooting and optimization of inventory workflows across distributed systems.</li>
            <li>Mentored and trained teams on automation tools, improving process efficiency by 25%.</li>
          </ul>
        </div>

        <div className="mt-4">
          <h3 className="font-bold">ModelN Software Pvt. Ltd.</h3>
          <p className="text-sm text-gray-600">Associate Consultant – Data Engineering (2020–2022)</p>
          <ul className="list-disc pl-5 text-sm mt-1 space-y-1">
            <li>Built data integration pipelines using Python, SQL, and API connectors to automate ingestion for MDM systems.</li>
            <li>Worked on healthcare and life sciences projects to unify and analyze revenue streams in real-time using BigQuery.</li>
            <li>Deployed scripts using Apache Airflow and integrated with GCP Dataflow for pipeline scheduling.</li>
          </ul>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Projects</h2>
        <div className="mt-4">
          <h3 className="font-bold">Stock Purchase Recommender Web App</h3>
          <p className="text-sm text-gray-600">Teesside University • 2022–2024</p>
          <ul className="list-disc pl-5 text-sm mt-1 space-y-1">
            <li>Built AI-powered recommender system using LSTM and regression-based models for stock predictions.</li>
            <li>Deployed frontend using Swift & Angular with backend pipeline connected to MySQL and BigQuery.</li>
            <li>Visualized insights with Tableau dashboards for live trade monitoring and user recommendations.</li>
          </ul>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Education</h2>
        <ul className="list-disc pl-5 mt-2 text-sm">
          <li>MSc in AI with Data Analytics – Teesside University, UK</li>
          <li>BTech in Computer Science (Data Science) – KL University, India</li>
        </ul>
      </section>

      <section>
        <h2 className="text-2xl font-semibold border-b pb-1">Contact</h2>
        <ul className="list-disc pl-5 mt-2 text-sm">
          <li>Email: sasimanchina@gmail.com</li>
          <li>LinkedIn: linkedin.com/in/manchina-bhavani-krishna-veni-62b6b0279</li>
          <li>Location: Bangalore, India</li>
        </ul>
      </section>
    </main>
  );
}
