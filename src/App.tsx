import { useState } from "react";
import "./App.css";

const programmingSkills = [
  "Python",
  "Back End",
  "Web Scraping",
  "REST APIs",
  "Relational Databases",
  "Concurrency",
  "Linux Server",
];

const pythonLibs = {
  mostUsed: [
    "Requests / HTTPX",
    "Pandas (everything?)",
    "Django (auth, ORM, views, migrations, admin, middleware)",
    "DRF (Model ViewSets, serializers, mixins)",
    "Asyncio",
    "Pydantic",
    "FastAPI",
  ],
  usedALot: ["Flask", "Selenium", "PySimpleGUI"],
};

const frontEndSkills = {
  introText:
    "It was not my focus at the beginning, but I had interest to learn how it works and I started to need more knowledge for some projects.",
  startedWith: [
    "Django Templating Language",
    "HTMX",
    "JS (very basic)",
    "Learning how to deliver bundled client-side JS (like Vite builds that came from other developers)",
  ],
  nowUsed: ["React", "TypeScript", "Tailwind", "Vite", "NextJS"],
};

const additionalSkillSlides = [
  {
    title: "Cloud APIs used",
    items: [
      "S3",
      "Azure Storage",
      "SharePoint via Azure App (GraphAPI)",
      "OpenAI (Live & Batch)",
    ],
  },
  {
    title: "Microsoft Office Skills",
    items: ["Power BI", "Power Query", "Excel (e.g. VLOOKUP)", "Power Automate"],
  },
];

const aboutParagraphs = [
  "I live in São Paulo - Brazil and have a background on Math and Statistics and I like these a lot.",
  "I started programming professionally by doing Web Scraping and some automations related to the extracted data.",
  "It evolved to more complex and bigger ETL processes that aimed to obtain and clear new data to the business analysts.",
  "I also was responsible for putting it on the Web as an easy-to-use system, as well to create new systems that facilitate some internal process or create a new layer of control and/or monitoring.",
  "I try to always put my thoughts and plans somewhere organized. I like Todoist, Basecamp, Obsidian or simple Google Docs.",
  "My goal is to create some tech solution that grows bigger than the internals of the company.",
];

const learningList = [
  "tRPC (or other easy way for the Front End to use (and see at their IDE) type-safe APIs)",
  "Bend / Interaction Combinators (I think I could have an application for its enumerating capabilities)",
  "Go: because I am feeling like it could be great to start coding in a compiled language",
];

const contactLinks = [
  { label: "Email", value: "filipeee0@gmail.com", href: "mailto:filipeee0@gmail.com" },
  { label: "GitHub", value: "Filipe-Araujo0", href: "https://github.com/Filipe-Araujo0" },
  {
    label: "LinkedIn",
    value: "Filipe da Silva Araujo",
    href: "https://www.linkedin.com/in/filipe-da-silva-araujo-08763916a/",
  },
];

function App(): JSX.Element {
  const [slideIndex, setSlideIndex] = useState(0);
  const totalSlides = additionalSkillSlides.length;

  const handlePrevious = () => {
    setSlideIndex((current) => (current === 0 ? totalSlides - 1 : current - 1));
  };

  const handleNext = () => {
    setSlideIndex((current) => (current === totalSlides - 1 ? 0 : current + 1));
  };

  return (
    <main className="page">
      <header className="hero">
        <h1 className="hero__title">Filipe</h1>
        <p className="hero__eyebrow">Software Engineer</p>
      </header>

      <section className="card">
        <h2>About me</h2>
        {aboutParagraphs.map((text) => (
          <p key={text}>{text}</p>
        ))}
      </section>

      <section className="card">
        <h2>Main Programming Skills</h2>
        <ul className="badge-grid">
          {programmingSkills.map((skill) => (
            <li key={skill} className="badge">
              {skill}
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h2>Python libs I use the most</h2>
        <div className="list-columns">
          <div>
            <h3>Used the most</h3>
            <ul>
              {pythonLibs.mostUsed.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Some that I used a lot</h3>
            <ul>
              {pythonLibs.usedALot.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Front End Skills</h2>
        <p>{frontEndSkills.introText}</p>
        <div className="list-columns">
          <div>
            <h3>I started with</h3>
            <ul>
              {frontEndSkills.startedWith.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Now I use</h3>
            <ul>
              {frontEndSkills.nowUsed.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Supporting toolset</h2>
        <div className="carousel" role="region" aria-label="Supporting toolset">
          <div className="carousel__controls">
            <button
              type="button"
              className="carousel__button"
              onClick={handlePrevious}
              aria-label="Previous slide"
            >
              <span aria-hidden="true">‹</span>
            </button>
            <span className="carousel__counter">
              {slideIndex + 1} / {totalSlides}
            </span>
            <button
              type="button"
              className="carousel__button"
              onClick={handleNext}
              aria-label="Next slide"
            >
              <span aria-hidden="true">›</span>
            </button>
          </div>
          <div className="carousel__viewport">
            <div
              className="carousel__track"
              style={{ transform: `translateX(-${slideIndex * 100}%)` }}
            >
              {additionalSkillSlides.map((slide, index) => (
                <article
                  key={slide.title}
                  className="carousel__slide"
                  aria-hidden={index !== slideIndex}
                  tabIndex={index === slideIndex ? 0 : -1}
                >
                  <h3>{slide.title}</h3>
                  <ul>
                    {slide.items.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Looking to learn</h2>
        <ol>
          {learningList.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ol>
      </section>

      <footer className="card">
        <h2>Contact</h2>
        <ul className="contact-list">
          {contactLinks.map((link) => (
            <li key={link.label}>
              <span className="contact-label">{link.label}:</span> {" "}
              <a href={link.href} target="_blank" rel="noreferrer">
                {link.value}
              </a>
            </li>
          ))}
        </ul>
      </footer>
    </main>
  );
}

export default App;
