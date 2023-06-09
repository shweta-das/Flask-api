import './App.css';
import React, { useEffect, useState } from 'react';
import axios from "axios";
const baseUrl = "http://localhost:5000"

function App() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [usersList, setUsersList] = useState([]);

  const handleChange = e => {
    setUsername(e.target.value);
    setPassword(e.target.value);
    setEmail(e.target.value);
  }

  const handleSubmit = async(e) => {
    e.preventDefault();
    try{
      const data = await axios.post(`${baseUrl}/users`, {username})
      setUsersList([...usersList, data.data]);
      setUsername('');
      setPassword('');
      setEmail('');
    }catch(err) {
      console.error(err.message);
    }
  }

  const fetchEvents = async () => {
    const data = await axios.get(`${baseUrl}/mgmt/users`)
    const {users} = data.data
    setUsersList(users);
  }

  useEffect(() => {
    fetchEvents();
  }, [])

  return (
    <div className="App">
      <section>
        <form onSubmit={handleSubmit}>
          <h2>Signup</h2>

          <label htmlFor="Username">Username</label>
          <input onChange={handleChange} type="text" name="username" id="username" value={username}></input>

          <label htmlFor="Password">Password</label>
          <input onChange={handleChange} type="password" name="password" id="password" value={password}></input>

          <label htmlFor="Email address">Email address</label>
          <input onChange={handleChange} type="text" name="email" id="email" value={email}></input>

          <button type="submit">Submit</button>
        </form>
      </section>
      <section>
        <ul>
          {usersList.map(user => {
            return (
              <li key={user}>{user.username} | {user.password} | {user.email}</li>
            ) }) } 
        </ul>
      </section>
    </div>
  );
}

export default App;
