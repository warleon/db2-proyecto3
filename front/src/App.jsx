import { useState ,useEffect} from 'react'
import SubmitForm from './components/SubmitForm/SubmitForm'
import PersonDisplay from './components/PersonDisplay/PersonDisplay'
import testdata from "./data"
import axios from 'axios';
import './App.css'

function App() {

  const [images, setImages] = useState([])


  useEffect(() => {
    console.log(images)
  },[images])

  const handleSubmit = (imagefile, topk) => {
    const url = 'api/analize'
    const formData = new FormData();
    formData.append('imagefile', imagefile);
    formData.append('topk', topk);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    }
    axios.post(url, formData, config).then((response) => setImages(response.data)); 
  }
  useEffect(()=>{console.log(images)},[images])

  return (
    <div className="App">
      <SubmitForm handleSubmit={handleSubmit}/>
      { images.length > 0 &&  images.map((imgarr, i) => {
        return <PersonDisplay index={i+1} images={imgarr}/>
      })}
    </div>
  )
}

export default App
