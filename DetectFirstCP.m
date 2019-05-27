
function [F,beg] = DetectFirstCP(R, epsilon)
	N = length(R);
	if N<=1, F=R; return; end;
	F = zeros(size(R)); 
	
    changepoints=[];
	F_low_first = R(1)-epsilon; 
	F_up_first = R(1)+epsilon; 	
	seglow = 1; 
	segup = 1;  
	segnum = 1; 
	indsegnum = 1; 
	firstlowind(1) = 1; 
	firstupind(1) = 1; 
    firstlowind=zeros(1,N); 
	firstupind=zeros(1,N); 
	F_lastlow = F_low_first; 
	F_lastup = F_up_first;
	for i = 2:N-1
	    if R(i)>=F_lastlow
	    	if R(i)<=F_lastup
		        F_lastup=F_lastup+(R(i)-F_lastup)/(i-firstupind(segup)+1);      
		        F(indsegnum)=F_up_first;
                changepoints=[changepoints,indsegnum];
                if indsegnum~=1
                    break
                end
		        while (segup>segnum)&&(F_lastup<=F(firstupind(segup-1)))
		        	segup=segup-1;
		        	F_lastup=F(firstupind(segup))+(F_lastup-F(firstupind(segup)))*...
		        		((i-firstupind(segup+1)+1)/(i-firstupind(segup)+1));
		        end
		        if segup==segnum,  
			        while (F_lastup<=F_low_first)&&(segnum<seglow)
				    	segnum=segnum+1;
				    	F(indsegnum:firstlowind(segnum)-1)=F_low_first;
				    	F_lastup=F_lastup+(F_lastup-F_low_first)*...
				    		((firstlowind(segnum)-indsegnum)/(i-firstlowind(segnum)+1));
				    	indsegnum=firstlowind(segnum);
				    	F_low_first=F(indsegnum);
	       			end
	    			F_up_first=F_lastup;
	    			segup=segnum;
	    			firstupind(segnum)=indsegnum;
	        	else, F(firstupind(segup))=F_lastup; end
	        else 
	        	segup=segup+1;
		        firstupind(segup)=i;
		        F(i)=R(i);
		        F_lastup=F(i);
	        end
	        F_lastlow=F_lastlow+(R(i)-F_lastlow)/(i-firstlowind(seglow)+1);      
	        F(indsegnum)=F_low_first;
	        while (seglow>segnum)&&(F_lastlow>=F(firstlowind(seglow-1)))
	        	seglow=seglow-1;
	        	F_lastlow=F(firstlowind(seglow))+(F_lastlow-F(firstlowind(seglow)))*...
	        		((i-firstlowind(seglow+1)+1)/(i-firstlowind(seglow)+1));
	        end
	        if seglow==segnum   
	        	while (F_lastlow>=F_up_first)&&(segnum<segup)
			    	segnum=segnum+1;
			    	F(indsegnum:firstupind(segnum)-1)=F_up_first;
			    	F_lastlow=F_lastlow+(F_lastlow-F_up_first)*...
			    		((firstupind(segnum)-indsegnum)/(i-firstupind(segnum)+1));
			    	indsegnum=firstupind(segnum);
			    	F_up_first=F(indsegnum);
	       		end
	       		F_low_first=F_lastlow;
	       		seglow=segnum;
	       		firstlowind(segnum)=indsegnum;
	       		if indsegnum==i, 
	       			F_low_first=F_up_first-2*epsilon;
	       		end; 
	        else, F(firstlowind(seglow))=F_lastlow; end
	    else
	       	seglow = seglow+1;
	        firstlowind(seglow) = i;
	        F(i)=R(i);
	        F_lastlow=F(i);
	        F_lastup=F_lastup+(R(i)-F_lastup)/(i-firstupind(segup)+1);      
	        F(indsegnum)=F_up_first;
	        while (segup>segnum)&&(F_lastup<=F(firstupind(segup-1)))
	        	segup=segup-1;
	        	F_lastup=F(firstupind(segup))+(F_lastup-F(firstupind(segup)))*...
	        		((i-firstupind(segup+1)+1)/(i-firstupind(segup)+1));
	        end
	        if segup==segnum   
	        	while (F_lastup<=F_low_first)&&(segnum<seglow) 
			    	segnum=segnum+1;
			    	F(indsegnum:firstlowind(segnum)-1)=F_low_first;
			    	F_lastup=F_lastup+(F_lastup-F_low_first)*...
			    		((firstlowind(segnum)-indsegnum)/(i-firstlowind(segnum)+1));
			    	indsegnum=firstlowind(segnum);
			    	F_low_first=F(indsegnum);

       			end
    			F_up_first=F_lastup;
    			segup=segnum;
    			firstupind(segnum)=indsegnum;
    			if indsegnum==i, 
    				F_up_first=F_low_first+2*epsilon;
    			end;
	        else, F(firstupind(segup))=F_lastup; end
	    end
	end
	i=N;
	if R(i)+epsilon<=F_lastlow 
        while segnum<seglow
	    	segnum=segnum+1;
	    	F(indsegnum:firstlowind(segnum)-1) = F_low_first;
	    	indsegnum=firstlowind(segnum);
	    	F_low_first=F(indsegnum);
     	end
     	F(indsegnum:i-1) = F_low_first;
     	F(i)=R(i)+epsilon;
    elseif R(i)-epsilon>=F_lastup 
		while segnum<segup
	    	segnum=segnum+1;
	    	F(indsegnum:firstupind(segnum)-1) = F_up_first;
	    	indsegnum=firstupind(segnum);
	    	F_up_first=F(indsegnum);
     	end
     	F(indsegnum:i-1) = F_up_first;
     	F(i)=R(i)-epsilon;
    else
        F_lastlow=F_lastlow+(R(i)+epsilon-F_lastlow)/(i-firstlowind(seglow)+1);      
        F(indsegnum)=F_low_first;
        while (seglow>segnum)&&(F_lastlow>=F(firstlowind(seglow-1)))
        	seglow=seglow-1;
        	F_lastlow=F(firstlowind(seglow))+(F_lastlow-F(firstlowind(seglow)))*...
        		((i-firstlowind(seglow+1)+1)/(i-firstlowind(seglow)+1));
        end
        if seglow==segnum 
        	if F_up_first>=F_lastlow 
        		F(indsegnum:i)=F_lastlow;
        	else
        		F_lastup=F_lastup+(R(i)-epsilon-F_lastup)/(i-firstupind(segup)+1);      
	        	F(indsegnum)=F_up_first;
	        	while (segup>segnum)&&(F_lastup<=F(firstupind(segup-1)))
	        		segup=segup-1;
	        		F_lastup=F(firstupind(segup))+(F_lastup-F(firstupind(segup)))*...
	        			((i-firstupind(segup+1)+1)/(i-firstupind(segup)+1));
	        	end
	       		F(firstupind(segup):i)=F_lastup;
        		while segnum<segup 
		    		segnum=segnum+1;
		    		F(indsegnum:firstupind(segnum)-1) = F_up_first;
		    		indsegnum=firstupind(segnum);
		    		F_up_first=F(indsegnum);
	     		end
	     	end
        else 	
        	F(firstlowind(seglow):i)=F_lastlow;
        	while segnum<seglow
		    	segnum=segnum+1;
		    	F(indsegnum:firstlowind(segnum)-1) = F_low_first;
		    	indsegnum=firstlowind(segnum);
		    	F_low_first=F(indsegnum);
	     	end
        end
    end
    beg=changepoints(changepoints~=1);
end	
