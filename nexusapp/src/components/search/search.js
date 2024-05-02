
import {NavLink, useParams} from "react-router-dom";
import { Link, useNavigate } from "react-router-dom"
import { useState, useMemo, useCallback, useEffect, useRef} from 'react';
import DataListInput from 'react-datalist-input';
import api from '../../api/axiosConfig'; 
import 'react-datalist-input/dist/styles.css'
import "./search.css"
import Pagination from "../Pagination";

const Search = () => {
    const [keywords, setKeywords] = useState("");
    const initialkeywords = useParams().initialkeywords;
    const navigate = useNavigate();
    const [serachRes,setserachRes]=useState([]);
    const [botsummary,setBotsummary]=useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 8;

  
    const options = [
        { name: 'how are glacier caves formed?' },
        { name: 'how did apollo creed die' },
        { name: 'how long is the term for federal judges' },
        { name: 'how a beretta model 21 pistols magazines' },
      ];  
      
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentItems = serachRes.slice(startIndex, endIndex);
    var dataReady = false;

    function handlePageChange(pageNumber) {
      setCurrentPage(pageNumber);
    }

    function searchInput(event){
        if (event.key === 'Enter') {
            navigate(`/search/${keywords}`);
            //clean bot_summary section
            setBotsummary("");
            sendQuery()
            console.log(keywords);
        }
    }
    const onSelectHistory = useCallback((selectedItem) => {   // The onSelect callback function is called if the user selects one option out of the search history.
        
      console.log('selectedItem', selectedItem);
      setKeywords(selectedItem.value)
      
    }, []);
    const searchHistory = useMemo(
        () =>
          options.map((option) => ({
            id: option.name,
            value: option.name,
          })),
        [],
      );

      const getsearch=async()=>{
        var response;
        debugger
        response = await api.post('/ad_search', {"term":keywords});
        
        if("msg" in response.data){
          setserachRes([]); 
        }  
        else{
          setserachRes(response.data["search_res"]); 
          localStorage.setItem("search_res",JSON.stringify(response.data["search_res"]));
          localStorage.setItem("query",keywords);
          dataReady = true;

        }      
      }

      const getBotsummary=async()=>{
        while(!dataReady){
          await new Promise(r => setTimeout(r, 500));
        }
        debugger
        const query =  localStorage.getItem("query");
        const serachRes = JSON.parse(localStorage.getItem("search_res"));
        var response = await api.post('/bot_summary', {"query":query,"search_res":serachRes})
        setBotsummary(response.data["bot_summary"]);
      }
      const sendQuery=()=>{
        dataReady = false;
        getsearch();
        getBotsummary();
      }
      const pageInitial=()=>{
        setKeywords(initialkeywords);
        sendQuery();
      }

    useEffect(() => {pageInitial();},[]);
    return(
        <div>
            <div className="search_board_container">
            <section className="search_board">
              <img src= "/logoBig.png" className="logo" alt="logo"></img>
              <img src= "/title.png" className="title" alt="title"></img>
              <section className="serach_bar_container">
                      <img src = "/search.png" className="searchicon" alg="icon"></img>
                      <DataListInput className="search_bar" placeholder="Search here" items={searchHistory}  onSelect={onSelectHistory} onKeyDown={searchInput} onChange={(e) => setKeywords(e.target.value)} />
              </section>
              <section className="bot_summary">
                  <img src="/bot.png" className="bot_img" alt="robot"></img>
                  <p>{botsummary}</p>
              </section>
              <section className="search_res_board">
                  <section className="search_res_list">
                  {currentItems?.map((page) => (
                    <div style={{"display":"flex","flex-direction":"column"}}>
                        <div className="search_res_item">
                            <h3 className="item_title">{page.title}</h3>
                          <p className="item_content">{page.content}</p>
                        </div>
                        <hr style={{"width":"70vw"}}/>
                    </div>      
                  ))}
                    </section>
                  </section>
                  <Pagination itemsPerPage={itemsPerPage}  data={serachRes} onPageChange={handlePageChange} />
            </section>
            <section className="sider">
                <img src="/sider.png" className="sider_img" alt="sider_img"></img>
            </section>
            
            </div>

        </div>
    );
}

export default Search;