function [F,CNVList] = IterativeTS(R, epsilon)

it=0;
pos=0;
F=[];
mm=R;
while length(mm)>0 
    epsilon=sqrt(var(mm)*2*log(length(mm))); 
    [F,beg] = DetectFirstCP(mm, epsilon) 
    mm=n((beg+pos(end)+1):length(R));
    pos=[pos,(beg+pos(end))];
    it=it+1;
    pos;
    s=F(1:beg);
    F=[F,s];
end
F=[F,repmat(mean(R((length(F)+1):end)),1,(length(n)-length(F)))];
pos=find(abs(diff(F))>0.1);
ipt=[pos];
in=find(diff(ipt)<100);
ipt(in)=[];
ipts=vec2mat(ipt,2);
mm=n;
denoised=[];
logcopR=[];
denoised(1:ipts(1,1)-1)=mean(mm(1:ipts(1,1)-1));
for f=1:length(ipt)-1
    denoised(ipt(f):ipt(f+1)-1)=mean(mm(ipt(f):ipt(f+1)-1));
    logcopR(f)=mean(mm(ipt(f):ipt(f+1)-1));
end
denoised(ipt(end):length(mm))=mean(mm(ipt(end):length(mm)));
logcopR=[mean(mm(1:ipts(1,1)-1)) logcopR mean(mm(ipt(end):length(mm)))];
start=[1 ipt];
stop=[ipt-1 length(mm)];
 
for g=1:size(ipts,1)
    logipt(g)=mean(mm(ipts(g,1):ipts(g,2)));
   
end
CNVlist = table(start',stop',logcopR','VariableNames',{'start' 'stop' 'Copynumber'});

end
