import { useState } from 'react';
import { useInterval } from './utils';

function App() {

  const [data, setData] = useState([]);

  useInterval(() => {
    fetch(process.env.REACT_APP_API_URL)
      .then(response => response.json())
      .then(response => setData(response))
  }, 1000)

  const unEpoch = epoch => {
    let d = new Date(epoch * 1000);
    return d.toLocaleString();
  }

  return (
    <div className="wrapper w-full">

      <h1 className="text-3xl pb-2 pl-2 font-bold text-slate-50 bg-gradient-to-r from-purple-500 to-pink-500 w-full">
        sensors
      </h1>

      <div className="flex flex-row flex-wrap w-full max-w-full box-border">
        {
          data != null && data.length > 0 ?
            data.map((target, i) => {
              return (
                <div
                  key={i}
                  className={
                    target["active"] ?
                      "p-4 w-1/4 m-4 bg-fuchsia-50 "
                      : "p-4 w-1/4 m-4"
                  }>
                  <h3>{target["host"]}</h3>
                  <h5>{unEpoch(target["last-update"])}</h5>
                  {
                    target["sensors"]["coretemp-isa-0000"]["Package id 0"] != null ?
                      <h3 className="text-xl font-bold">{target["sensors"]["coretemp-isa-0000"]["Package id 0"]["temp1_input"]}°C</h3>
                      :
                      <h3 className="text-xl font-bold">{target["sensors"]["coretemp-isa-0000"]["Core 0"]["temp2_input"]}°C</h3>
                  }
                </div>
              )
            })
            : null
        }
      </div>


    </div>
  );
}

export default App;
