import './App.css'; //This imports a CSS file to style the app.
import api from './api/axiosConfig'; //This imports an API instance from the axiosConfig.js file in the api directory.
import {useState, useEffect} from 'react'; //This imports the useState and useEffect hooks from the React library.
import {Routes, Route} from 'react-router-dom';
import Search from "./components/search/search.js";

function App() {
  return (
    <div className="App">
        <Routes>
          <Route path="/search/:initialkeywords" element={<Search/>}></Route>
        </Routes>
    </div>
  );
}

export default App;




