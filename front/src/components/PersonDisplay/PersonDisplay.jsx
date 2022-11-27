import "./PersonDisplay.css"

function PersonDisplay({ images, index }) {

    return (
        <div className="person-cont">
            <hr className="person-hr"></hr>
            <span className="person-title">Person {index}</span>
            <div className="person-imgs-cont">
                {
                images.map((item) => {
                    return <div className="img-score-cont"><div style={{backgroundImage: `url(${"api/"+item.image})`}} className="person-img"></div><span className="img-score-text">Score: {item.distance.toFixed(4)}</span></div>
                })}
            </div>
        </div>
    )
}

export default PersonDisplay