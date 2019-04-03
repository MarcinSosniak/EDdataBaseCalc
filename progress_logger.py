


class ProgressLogger:
    def __init__(self,total_steps,print_amount=100,name=""):
        self._msg=name
        self._n=total_steps
        self._max_shows=print_amount
        self._prints=0
        self._progres=0
        self._progres_threshold=int(self._n/self._max_shows)

    def log_step(self):
        self._progres=self._progres+1
        if(self._progres>=self._progres_threshold):
            self._progres=0
            self._prints=self._prints+1
            prcnt=(float(self._prints)/float(self._max_shows))*100
            print(self._msg+" progress: "+str(prcnt)+"%")