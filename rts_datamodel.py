from base_model import DataModel

class RTSDataModel(DataModel):
    
    def get_rt_stocks():
    	def parsing_web(code):
        	url = 'http://stock.daum.net/item/main.daum?code=' + code
        	soup = BeautifulSoup(urllib.urlopen(url).read())
        return soup.find("ul", "list_stockrate").contents[1].contents[0].encode_contents()

    	for stock in stock_list:
        	TaskController().enqueue_task(Task(parsing_web, stock))
        
        self.add_data(TaskController().deque_task(), True)
