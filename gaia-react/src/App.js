import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [anagram, setAnagram] = useState("");
  const [anagramResult, setAnagramResult] = useState("");
  const [dictionaryData, setDictionaryData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);

  const isFirstRun = useRef(true);
  useEffect(() => {
    if (isFirstRun.current) {
      isFirstRun.current = false; //i'm using useRef to not run this code on the first run
      return;
    }

    const fetchData = async () => {
      setIsLoading(true);

      try {
        const result = await axios.get(
          `http://dicionario-aberto.net/search-json/${anagramResult}`
        );
        setIsLoading(false);
        if (result.status === 200) {
          setDictionaryData(result.data);
          setError(false);
        } else {
          setDictionaryData({});
          setError(true);
        }
      } catch (error) {
        setDictionaryData({});
        setError(true);
        setIsLoading(false);
        console.log(error);
      }
    };
    fetchData();
  }, [anagramResult]);

  const reverseWord = word => {
    setAnagramResult([...word].reverse().join``);
  };

  return (
    <div className="App">
      <input
        type="text"
        name="anagram"
        onChange={e => setAnagram(e.target.value)}
        value={anagram}
      />
      <button onClick={() => reverseWord(anagram)}>Check Anagram</button>
      <p>result: {anagramResult}</p>
      {isLoading && <p>Loading...</p>}
      {!isLoading && dictionaryData.entry && (
        <div>
          <p>Definições: {dictionaryData.entry.sense[1].def}</p>
          <p>{dictionaryData.entry.sense[2].def}</p>
          <p>{dictionaryData.entry.sense[3].def}</p>
        </div>
      )}
      {error ? <p>Houve um erro na pesquisa ou a palavra não existe.</p> : null}
    </div>
  );
}

export default App;
