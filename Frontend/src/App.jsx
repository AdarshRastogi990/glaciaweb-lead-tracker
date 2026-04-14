import { useState, useEffect } from 'react'
import './App.css'

function App() {
  // 1. STATE (Memory): leads ki list aur form ka data save karne ke liye
  const [leads, setLeads] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    service_required: '',
    status: 'Pending'
  });
  const [message, setMessage] = useState(''); // Error ya success message dikhane ke liye

  // 2. USE EFFECT: Page load hote hi backend se data mangwana
  useEffect(() => {
    fetchLeads();
  }, []); // Khali bracket [] ka matlab hai ki ye sirf pehli baar load hone par chalega

  // GET Request: Backend se saare leads lane ka function
  const fetchLeads = async () => {
    try {
      // fetch ek postman hai jo is URL par jaakar data laya
      const response = await fetch('http://127.0.0.1:5000/api/leads');
      const data = await response.json();
      setLeads(data); // Jo data aaya, use apni memory (state) mein save kar liya
    } catch (error) {
      console.error("Error fetching leads:", error);
    }
  };

  // Jab user form mein kuch type karega, toh ye function memory (formData) ko update karega
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData, // Purana data waisa hi rakho
      [name]: value // Sirf wo field update karo jo user abhi type kar raha hai
    });
  };

  // POST Request: Jab user 'Add Lead' button dabayega
  const handleSubmit = async (e) => {
    e.preventDefault(); // Form submit hone par page ko reload hone se rokna
    setMessage('');

    try {
      // API ko naya data bhejna
      const response = await fetch('http://127.0.0.1:5000/api/leads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // JavaScript object ko JSON text mein badalna
      });

      const result = await response.json();

      if (response.ok) {
        setMessage("Lead added successfully!");
        setFormData({ name: '', email: '', service_required: '', status: 'Pending' }); // Form ko khali kar do
        fetchLeads(); // Table ko update karne ke liye naya data phir se mangwao
      } else {
        // Agar backend ne validation error diya (jaise email format galat hai)
        setMessage(`Error: ${result.error}`);
      }
    } catch (error) {
      setMessage("System error: Could not connect to backend.");
    }
  };

  return (
    <div className="dashboard-container">
      <h1>GlaciaWeb Lead Tracker</h1>
      
      {/* Agar koi message hai toh use screen par dikhao */}
      {message && <div className="message-box">{message}</div>}

      {/* FORM SECTION */}
      <div className="form-section">
        <h2>Add New Client Lead</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            name="name" 
            placeholder="Client Name" 
            value={formData.name} 
            onChange={handleInputChange} 
            required 
          />
          <input 
            type="email" 
            name="email" 
            placeholder="Email Address" 
            value={formData.email} 
            onChange={handleInputChange} 
            required 
          />
          <select name="service_required" value={formData.service_required} onChange={handleInputChange}>
            <option value="">Select Service</option>
            <option value="Web Development">Web Development</option>
            <option value="SEO & Marketing">SEO & Marketing</option>
            <option value="UI/UX Design">UI/UX Design</option>
          </select>
          <button type="submit">Add Lead</button>
        </form>
      </div>

      {/* TABLE SECTION */}
      <div className="table-section">
        <h2>Current Leads</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Service</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {/* leads array mein ghoom-ghoom kar (map) har lead ke liye ek row banana */}
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td>{lead.id}</td>
                <td>{lead.name}</td>
                <td>{lead.email}</td>
                <td>{lead.service_required}</td>
                <td><span className={`status-badge ${lead.status.toLowerCase()}`}>{lead.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App
