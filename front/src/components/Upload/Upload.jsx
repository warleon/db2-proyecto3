import "./Upload.css"
import person from "../../assets/person.png"

function Upload({ selectedImage, handleImageUpload }) {

    return (
        <div className="upload-cont">
            {selectedImage ? <img className="display-img" src={URL.createObjectURL(selectedImage)} /> : <img className="display-img" src={person} />}
            <input className="display-input" type="file" name="selectedImage" onChange={handleImageUpload} />
        </div>
    )
}

export default Upload;