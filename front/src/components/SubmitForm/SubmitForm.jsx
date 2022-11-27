import { useState } from 'react'
import Upload from '../Upload/Upload'
import './SubmitForm.css'

function SubmitForm({ handleSubmit }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [topk, setTopk] = useState(0)

  const handleImageUpload = (event) => {
    setSelectedImage(event.target.files[0]);
  }

  return (
    <div className="sf-cont">
      <Upload handleImageUpload={handleImageUpload} selectedImage={selectedImage}/>
      <div className="topk-submit">
        <span className='topk-label'>Top-k:</span>
        <input className='topk-input' value={topk} onChange={(e) => {setTopk(e.target.value)}} type="number"/>
        <button className='sf-submit' onClick={() => {handleSubmit(selectedImage, topk)}}>Submit</button>
      </div>
    </div>
  )
}

export default SubmitForm
