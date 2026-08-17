import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // =========================================================
  // STATE
  // =========================================================

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  const [profile, setProfile] = useState(null);
  const [job, setJob] = useState(null);
  const [matchResult, setMatchResult] = useState(null);

  const [roadmap, setRoadmap] = useState(null);
  const [tailoredResume, setTailoredResume] = useState(null);
  const [coverLetter, setCoverLetter] = useState(null);

  const [interviewSet, setInterviewSet] = useState(null);
  const [interviewAnswers, setInterviewAnswers] = useState(null);

  const [loading, setLoading] = useState(false);
  const [matchLoading, setMatchLoading] = useState(false);
  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [resumeLoading, setResumeLoading] = useState(false);
  const [coverLetterLoading, setCoverLetterLoading] = useState(false);
  const [interviewLoading, setInterviewLoading] = useState(false);
  const [answersLoading, setAnswersLoading] = useState(false);

  const [error, setError] = useState("");

  // =========================================================
  // RESUME ANALYSIS
  // =========================================================

  const analyzeResume = async () => {
    if (!resumeFile) {
      setError("Please select a PDF or DOCX resume first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();

      formData.append("file", resumeFile);

      const response = await axios.post(
        `${API_URL}/profile/analyze`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setProfile(response.data.profile);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Something went wrong while analyzing the resume."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // JOB DESCRIPTION ANALYSIS
  // =========================================================

  const analyzeJobDescription = async () => {
    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/jobs/analyze`,
        {
          job_description: jobDescription,
        }
      );

      setJob(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to analyze the job description."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // JOB MATCHING
  // =========================================================

  const matchCandidate = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    setMatchLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${API_URL}/jobs/match`,
        {
          candidate: profile,
          job: job,
        }
      );

      setMatchResult(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to calculate the job match."
      );
    } finally {
      setMatchLoading(false);
    }
  };

  // =========================================================
  // LEARNING ROADMAP
  // =========================================================

  const generateRoadmap = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    setRoadmapLoading(true);
    setError("");

    try {
      const currentSkills = profile.skills || [];

      const requiredSkills = [
        ...(job.required_skills || []),
        ...(job.preferred_skills || []),
      ];

      const currentSkillSet = new Set(
        currentSkills.map((skill) => skill.toLowerCase())
      );

      const skillGaps = requiredSkills.filter(
        (skill) =>
          !currentSkillSet.has(skill.toLowerCase())
      );

      const response = await axios.post(
        `${API_URL}/roadmap/generate`,
        {
          target_role:
            job.job_title || "Software Engineer",

          current_skills: currentSkills,

          skill_gaps: skillGaps,

          total_days: 7,
        }
      );

      setRoadmap(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate the learning roadmap."
      );
    } finally {
      setRoadmapLoading(false);
    }
  };

  // =========================================================
  // TAILOR RESUME
  // =========================================================

  const generateTailoredResume = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    setResumeLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${API_URL}/resume/tailor`,
        {
          candidate: profile,
          job: job,
        }
      );

      setTailoredResume(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate the tailored resume."
      );
    } finally {
      setResumeLoading(false);
    }
  };

  // =========================================================
  // COVER LETTER
  // =========================================================

  const generateCoverLetter = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    setCoverLetterLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${API_URL}/cover-letter/generate`,
        {
          candidate: profile,
          job: job,
        }
      );

      setCoverLetter(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate the cover letter."
      );
    } finally {
      setCoverLetterLoading(false);
    }
  };

  // =========================================================
  // INTERVIEW QUESTIONS
  // =========================================================

  const generateInterview = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    setInterviewLoading(true);
    setError("");

    try {
      const currentSkills = profile.skills || [];

      const requiredSkills = [
        ...(job.required_skills || []),
        ...(job.preferred_skills || []),
      ];

      const currentSkillSet = new Set(
        currentSkills.map((skill) => skill.toLowerCase())
      );

      const skillGaps = requiredSkills.filter(
        (skill) =>
          !currentSkillSet.has(skill.toLowerCase())
      );

      const response = await axios.post(
        `${API_URL}/interview/generate`,
        {
          candidate: profile,
          job: job,
          skill_gaps: skillGaps,
        }
      );

      setInterviewSet(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate interview questions."
      );
    } finally {
      setInterviewLoading(false);
    }
  };

  // =========================================================
  // INTERVIEW ANSWERS
  // =========================================================

  const generateInterviewAnswers = async () => {
    if (!profile) {
      setError("Please analyze your resume first.");
      return;
    }

    if (!job) {
      setError("Please analyze the job description first.");
      return;
    }

    if (!interviewSet) {
      setError("Please generate interview questions first.");
      return;
    }

    setAnswersLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `${API_URL}/interview/answers`,
        {
          candidate: profile,
          job: job,
          interview_set: interviewSet,
        }
      );

      setInterviewAnswers(response.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate interview answers."
      );
    } finally {
      setAnswersLoading(false);
    }
  };

  // =========================================================
  // HELPER
  // =========================================================

  const formatValue = (value) => {
    if (value === null || value === undefined) {
      return "Not provided";
    }

    if (Array.isArray(value)) {
      return value.join(", ");
    }

    return value;
  };

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="app">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <header className="header">

        <div className="logo">

          <div className="logo-icon">
            🚀
          </div>

          <div>
            <h1>
              CareerPilot AI
            </h1>

            <p>
              AI-Powered Career & Placement Assistant
            </p>
          </div>

        </div>

      </header>


      {/* ================================================= */}
      {/* HERO */}
      {/* ================================================= */}

      <section className="hero">

        <div className="hero-content">

          <span className="hero-badge">
            AI CAREER ASSISTANT
          </span>

          <h2>
            Build Your Career
            <span> Smarter</span>
          </h2>

          <p>
            Upload your resume and let CareerPilot AI
            analyze your profile, identify skill gaps,
            and prepare you for your target role.
          </p>

        </div>

      </section>


      <main className="container">

        {/* ================================================= */}
        {/* ERROR */}
        {/* ================================================= */}

        {error && (
          <div className="error-box">

            <strong>
              Error:
            </strong>{" "}

            {error}

          </div>
        )}


        {/* ================================================= */}
        {/* INPUT SECTION */}
        {/* ================================================= */}

        <section className="input-section">

          {/* RESUME */}

          <div className="input-card">

            <div className="section-icon">
              📄
            </div>

            <h2>
              Resume Analysis
            </h2>

            <p>
              Upload your latest resume in PDF or DOCX format.
            </p>

            <label className="file-input">

              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(event) =>
                  setResumeFile(
                    event.target.files[0]
                  )
                }
              />

              <span>
                Choose your Resume
              </span>

            </label>

            {resumeFile && (
              <p className="selected-file">

                Selected:{" "}

                <strong>
                  {resumeFile.name}
                </strong>

              </p>
            )}

            <button
              className="primary-button"
              onClick={analyzeResume}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze My Profile"}
            </button>

          </div>


          {/* JOB DESCRIPTION */}

          <div className="input-card">

            <div className="section-icon">
              💼
            </div>

            <h2>
              Job Description
            </h2>

            <p>
              Paste the job description for your target role.
            </p>

            <textarea
              className="job-textarea"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(event) =>
                setJobDescription(
                  event.target.value
                )
              }
            />

            <button
              className="primary-button"
              onClick={analyzeJobDescription}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Analyze Job Description"}
            </button>

          </div>

        </section>


        {/* ================================================= */}
        {/* PROFILE RESULT */}
        {/* ================================================= */}

        {profile && (

          <section className="result-card">

            <div className="result-title">

              <span>
                👤
              </span>

              <div>

                <h2>
                  Candidate Profile
                </h2>

                <p>
                  Information extracted from your resume
                </p>

              </div>

            </div>


            <div className="profile-grid">

              <div className="profile-item">

                <span>
                  Name
                </span>

                <strong>
                  {formatValue(profile.name)}
                </strong>

              </div>


              <div className="profile-item">

                <span>
                  Email
                </span>

                <strong>
                  {formatValue(profile.email)}
                </strong>

              </div>


              <div className="profile-item">

                <span>
                  Phone
                </span>

                <strong>
                  {formatValue(profile.phone)}
                </strong>

              </div>

            </div>


            {profile.skills?.length > 0 && (

              <div className="profile-section">

                <h3>
                  Technical Skills
                </h3>

                <div className="skill-list">

                  {profile.skills.map(
                    (skill, index) => (

                      <span
                        className="skill-tag"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            )}

          </section>

        )}


        {/* ================================================= */}
        {/* JOB RESULT */}
        {/* ================================================= */}

        {job && (

          <section className="result-card">

            <div className="result-title">

              <span>
                💼
              </span>

              <div>

                <h2>
                  Job Profile
                </h2>

                <p>
                  Requirements extracted from the job description
                </p>

              </div>

            </div>


            <div className="profile-grid">

              <div className="profile-item">

                <span>
                  Job Title
                </span>

                <strong>
                  {formatValue(job.job_title)}
                </strong>

              </div>


              <div className="profile-item">

                <span>
                  Company
                </span>

                <strong>
                  {formatValue(job.company)}
                </strong>

              </div>


              <div className="profile-item">

                <span>
                  Location
                </span>

                <strong>
                  {formatValue(job.location)}
                </strong>

              </div>

            </div>


            <div className="job-skills">

              <div>

                <h3>
                  Required Skills
                </h3>

                <div className="skill-list">

                  {(job.required_skills || []).map(
                    (skill, index) => (

                      <span
                        className="skill-tag required"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>


              <div>

                <h3>
                  Preferred Skills
                </h3>

                <div className="skill-list">

                  {(job.preferred_skills || []).map(
                    (skill, index) => (

                      <span
                        className="skill-tag preferred"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            </div>

          </section>

        )}


        {/* ================================================= */}
        {/* FEATURE CARDS */}
        {/* ================================================= */}

        <section className="features">

          <div className="section-heading">

            <h2>
              Career Tools
            </h2>

            <p>
              Use AI-powered tools to prepare for your target role.
            </p>

          </div>


          <div className="feature-grid">


            {/* JOB MATCH */}

            <div className="feature-card">

              <div className="feature-icon">
                🎯
              </div>

              <h3>
                Job Match
              </h3>

              <p>
                Compare your skills with the
                requirements of your target job.
              </p>

              <button
                className="secondary-button"
                onClick={matchCandidate}
                disabled={matchLoading}
              >
                {matchLoading
                  ? "Matching..."
                  : "Match My Profile"}
              </button>

            </div>


            {/* ROADMAP */}

            <div className="feature-card">

              <div className="feature-icon">
                🗺️
              </div>

              <h3>
                Learning Roadmap
              </h3>

              <p>
                Get a personalized learning plan
                based on your skill gaps.
              </p>

              <button
                className="secondary-button"
                onClick={generateRoadmap}
                disabled={roadmapLoading}
              >
                {roadmapLoading
                  ? "Generating..."
                  : "Generate Roadmap"}
              </button>

            </div>


            {/* TAILORED RESUME */}

            <div className="feature-card">

              <div className="feature-icon">
                📝
              </div>

              <h3>
                Tailored Resume
              </h3>

              <p>
                Create a job-focused resume using
                your existing profile.
              </p>

              <button
                className="secondary-button"
                onClick={generateTailoredResume}
                disabled={resumeLoading}
              >
                {resumeLoading
                  ? "Generating..."
                  : "Tailor My Resume"}
              </button>

            </div>


            {/* COVER LETTER */}

            <div className="feature-card">

              <div className="feature-icon">
                ✉️
              </div>

              <h3>
                Cover Letter
              </h3>

              <p>
                Generate a personalized cover letter
                for your target job.
              </p>

              <button
                className="secondary-button"
                onClick={generateCoverLetter}
                disabled={coverLetterLoading}
              >
                {coverLetterLoading
                  ? "Generating..."
                  : "Generate Cover Letter"}
              </button>

            </div>


            {/* INTERVIEW */}

            <div className="feature-card">

              <div className="feature-icon">
                🎤
              </div>

              <h3>
                Interview Questions
              </h3>

              <p>
                Generate technical, project,
                and behavioral interview questions.
              </p>

              <button
                className="secondary-button"
                onClick={generateInterview}
                disabled={interviewLoading}
              >
                {interviewLoading
                  ? "Generating..."
                  : "Generate Questions"}
              </button>

            </div>


            {/* INTERVIEW ANSWERS */}

            <div className="feature-card">

              <div className="feature-icon">
                💡
              </div>

              <h3>
                Interview Answers
              </h3>

              <p>
                Generate concise answers and
                interview tips for your questions.
              </p>

              <button
                className="secondary-button"
                onClick={generateInterviewAnswers}
                disabled={answersLoading}
              >
                {answersLoading
                  ? "Generating..."
                  : "Generate Answers"}
              </button>

            </div>

          </div>

        </section>


        {/* ================================================= */}
        {/* MATCH RESULT */}
        {/* ================================================= */}

        {matchResult && (

          <section className="result-card">

            <div className="result-title">

              <span>
                🎯
              </span>

              <div>

                <h2>
                  Job Match Result
                </h2>

                <p>
                  Your compatibility with the target role
                </p>

              </div>

            </div>


            <div className="match-score">

              <div className="score-circle">

                <strong>

                  {matchResult.match_percentage ??
                    matchResult.match_score ??
                    matchResult.score ??
                    0}

                  %

                </strong>

              </div>

            </div>


            {matchResult.matched_required_skills?.length > 0 && (

              <div className="profile-section">

                <h3>
                  Matched Required Skills
                </h3>

                <div className="skill-list">

                  {matchResult.matched_required_skills.map(
                    (skill, index) => (

                      <span
                        className="skill-tag"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            )}


            {matchResult.missing_required_skills?.length > 0 && (

              <div className="profile-section">

                <h3>
                  Missing Required Skills
                </h3>

                <div className="skill-list">

                  {matchResult.missing_required_skills.map(
                    (skill, index) => (

                      <span
                        className="skill-tag gap"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            )}


            {matchResult.matched_preferred_skills?.length > 0 && (

              <div className="profile-section">

                <h3>
                  Matched Preferred Skills
                </h3>

                <div className="skill-list">

                  {matchResult.matched_preferred_skills.map(
                    (skill, index) => (

                      <span
                        className="skill-tag preferred"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            )}


            {matchResult.skill_gaps?.length > 0 && (

              <div className="profile-section">

                <h3>
                  Skill Gaps
                </h3>

                <div className="skill-list">

                  {matchResult.skill_gaps.map(
                    (skill, index) => (

                      <span
                        className="skill-tag gap"
                        key={index}
                      >
                        {skill}
                      </span>

                    )
                  )}

                </div>

              </div>

            )}


            {matchResult.recommendation && (

              <div className="interview-tip">

                <strong>
                  💡 Recommendation
                </strong>

                <p>
                  {matchResult.recommendation}
                </p>

              </div>

            )}

          </section>

        )}


        {/* ================================================= */}
        {/* ROADMAP */}
        {/* ================================================= */}

        {roadmap && (

          <section className="result-card">

            <div className="result-title">

              <span>
                🗺️
              </span>

              <div>

                <h2>
                  Learning Roadmap
                </h2>

                <p>
                  Your personalized learning plan
                </p>

              </div>

            </div>


            <div className="roadmap-summary">

              <div>

                <span>
                  Target Role
                </span>

                <strong>
                  {roadmap.target_role}
                </strong>

              </div>

              <div>

                <span>
                  Duration
                </span>

                <strong>
                  {roadmap.total_days} Days
                </strong>

              </div>

            </div>


            <div className="roadmap-list">

              {(roadmap.roadmap || []).map(
                (day, index) => (

                  <div
                    className="roadmap-day"
                    key={index}
                  >

                    <div className="day-number">
                      Day {day.day}
                    </div>

                    <div className="day-content">

                      <h3>
                        {day.skill}
                      </h3>

                      {day.topics?.length > 0 && (

                        <div>

                          <h4>
                            Topics
                          </h4>

                          <ul>

                            {day.topics.map(
                              (topic, topicIndex) => (

                                <li
                                  key={topicIndex}
                                >
                                  {topic}
                                </li>

                              )
                            )}

                          </ul>

                        </div>

                      )}

                      {day.tasks?.length > 0 && (

                        <div>

                          <h4>
                            Tasks
                          </h4>

                          <ul>

                            {day.tasks.map(
                              (task, taskIndex) => (

                                <li
                                  key={taskIndex}
                                >
                                  {task}
                                </li>

                              )
                            )}

                          </ul>

                        </div>

                      )}

                    </div>

                  </div>

                )
              )}

            </div>

          </section>

        )}


        {/* ================================================= */}
        {/* TAILORED RESUME */}
        {/* ================================================= */}

        {tailoredResume && (

          <section className="result-card">

            <div className="result-title">

              <span>
                📝
              </span>

              <div>

                <h2>
                  Tailored Resume
                </h2>

                <p>
                  Resume optimized for your target role
                </p>

              </div>

            </div>


            <div className="resume-preview">

              <h2>
                {tailoredResume.name}
              </h2>

              <p>
                {tailoredResume.email}
              </p>

              <p>
                {tailoredResume.phone}
              </p>


              {tailoredResume.professional_summary && (

                <div className="resume-section">

                  <h3>
                    Professional Summary
                  </h3>

                  <p>
                    {tailoredResume.professional_summary}
                  </p>

                </div>

              )}


              {tailoredResume.skills?.length > 0 && (

                <div className="resume-section">

                  <h3>
                    Skills
                  </h3>

                  <div className="skill-list">

                    {tailoredResume.skills.map(
                      (skill, index) => (

                        <span
                          className="skill-tag"
                          key={index}
                        >
                          {skill}
                        </span>

                      )
                    )}

                  </div>

                </div>

              )}


              {tailoredResume.education?.length > 0 && (

                <div className="resume-section">

                  <h3>
                    Education
                  </h3>

                  {tailoredResume.education.map(
                    (education, index) => (

                      <div
                        className="education-item"
                        key={index}
                      >

                        <strong>
                          {education.institution}
                        </strong>

                        <p>
                          {education.degree}{" "}

                          {education.field_of_study
                            ? `in ${education.field_of_study}`
                            : ""}
                        </p>

                        <p>
                          {education.year}{" "}
                          {education.score}
                        </p>

                      </div>

                    )
                  )}

                </div>

              )}


              {tailoredResume.projects?.length > 0 && (

                <div className="resume-section">

                  <h3>
                    Projects
                  </h3>

                  {tailoredResume.projects.map(
                    (project, index) => (

                      <div
                        className="project-item"
                        key={index}
                      >

                        <h4>
                          {project.name}
                        </h4>

                        <p>
                          {project.description}
                        </p>

                        {project.technologies && (

                          <div className="skill-list">

                            {project.technologies.map(
                              (technology, technologyIndex) => (

                                <span
                                  className="skill-tag"
                                  key={technologyIndex}
                                >
                                  {technology}
                                </span>

                              )
                            )}

                          </div>

                        )}

                      </div>

                    )
                  )}

                </div>

              )}

            </div>

          </section>

        )}


        {/* ================================================= */}
        {/* COVER LETTER */}
        {/* ================================================= */}

        {coverLetter && (

          <section className="result-card">

            <div className="result-title">

              <span>
                ✉️
              </span>

              <div>

                <h2>
                  Cover Letter
                </h2>

                <p>
                  Personalized application letter
                </p>

              </div>

            </div>


            <div className="cover-letter">

              <h3>
                {coverLetter.subject}
              </h3>

              <p>

                <strong>
                  To:
                </strong>{" "}

                {coverLetter.recipient}

              </p>

              <p>
                {coverLetter.greeting}
              </p>


              {coverLetter.body
                ?.split("\n\n")
                .map(
                  (paragraph, index) => (

                    <p key={index}>
                      {paragraph}
                    </p>

                  )
                )}


              <p className="closing">
                {coverLetter.closing}
              </p>

            </div>

          </section>

        )}


        {/* ================================================= */}
        {/* INTERVIEW QUESTIONS */}
        {/* ================================================= */}

        {interviewSet && (

          <section className="result-card">

            <div className="result-title">

              <span>
                🎤
              </span>

              <div>

                <h2>
                  Interview Questions
                </h2>

                <p>
                  Questions generated for your target role
                </p>

              </div>

            </div>


            <div className="interview-list">

              {(interviewSet.questions || []).map(
                (question, index) => (

                  <div
                    className="interview-question"
                    key={index}
                  >

                    <div className="question-number">
                      {index + 1}
                    </div>

                    <div className="question-content">

                      <h3>
                        {question.question}
                      </h3>

                      <div className="question-meta">

                        <span>
                          {question.category}
                        </span>

                        <span>
                          {question.difficulty}
                        </span>

                      </div>


                      {question.expected_topics?.length > 0 && (

                        <div className="expected-topics">

                          <strong>
                            Expected Topics:
                          </strong>{" "}

                          {question.expected_topics.join(
                            ", "
                          )}

                        </div>

                      )}

                    </div>

                  </div>

                )
              )}

            </div>


            <button
              className="primary-button interview-answer-button"
              onClick={generateInterviewAnswers}
              disabled={answersLoading}
            >
              {answersLoading
                ? "Generating Answers..."
                : "Generate Interview Answers"}
            </button>

          </section>

        )}


        {/* ================================================= */}
        {/* INTERVIEW ANSWERS */}
        {/* ================================================= */}

        {interviewAnswers && (

          <section className="result-card">

            <div className="result-title">

              <span>
                💡
              </span>

              <div>

                <h2>
                  Interview Answers
                </h2>

                <p>
                  Personalized preparation answers and tips
                </p>

              </div>

            </div>


            <div className="answers-list">

              {(interviewAnswers.answers || []).map(
                (item, index) => (

                  <div
                    className="answer-card"
                    key={index}
                  >

                    <div className="answer-number">
                      Question {index + 1}
                    </div>

                    <h3>
                      {item.question}
                    </h3>


                    <div className="answer-box">

                      <strong>
                        Answer
                      </strong>

                      <p>
                        {item.answer}
                      </p>

                    </div>


                    {item.key_points?.length > 0 && (

                      <div className="key-points">

                        <strong>
                          Key Points
                        </strong>

                        <ul>

                          {item.key_points.map(
                            (point, pointIndex) => (

                              <li
                                key={pointIndex}
                              >
                                {point}
                              </li>

                            )
                          )}

                        </ul>

                      </div>

                    )}


                    {item.interview_tip && (

                      <div className="interview-tip">

                        <strong>
                          💡 Interview Tip
                        </strong>

                        <p>
                          {item.interview_tip}
                        </p>

                      </div>

                    )}

                  </div>

                )
              )}

            </div>

          </section>

        )}

      </main>


      {/* ================================================= */}
      {/* FOOTER */}
      {/* ================================================= */}

      <footer className="footer">

        <p>
          🚀 CareerPilot AI
        </p>

        <span>
          AI-Powered Career & Placement Assistant
        </span>

      </footer>

    </div>
  );
}

export default App;