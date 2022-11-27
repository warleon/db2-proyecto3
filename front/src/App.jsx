import { useState } from 'react'
import SubmitForm from './components/SubmitForm/SubmitForm'
import PersonDisplay from './components/PersonDisplay/PersonDisplay'
import testdata from "./data"
import axios from 'axios';
import './App.css'

function App() {

  const [images, setImages] = useState([])

  const handleSubmit = (imagefile, topk) => {
    const url = 'api/???';
    const formData = new FormData();
    formData.append('imagefile', imagefile);
    formData.append('topk', topk);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    }
    console.log(formData.get("imagefile"))
    console.log(formData.get("topk"))
    console.log(config)
    /* axios.post(url, formData, config).then((response) => setImages(response.data)); */
  }

  return (
    <div className="App">
      <SubmitForm handleSubmit={handleSubmit}/>
      {/* images.length > 0 &&  */testdata.map((imgarr, i) => {
        return <PersonDisplay index={i+1} images={imgarr}/>
      })}
    </div>
  )
}

export default App
