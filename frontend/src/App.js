import React from "react"
import {BrowserRouter as Router, Route, Routes, useNavigate} from 'react-router-dom';
import AllMasters from "./components/MainPage/AllMasters"
import LoginUser from "./components/LoginPage/LoginUser"

function App() {
  return(
    <Router>
      <Routes>
          <Route path='/' element={<AllMasters />}/>
          <Route path='/login' element={<LoginUser/>}/>
      </Routes>
    </Router>
  )
};

export default App;