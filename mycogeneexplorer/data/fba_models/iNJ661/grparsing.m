bleh=regexp(ChidelevitchModel.grRules,'(');
blehR=regexp(ChidelevitchModel.grRules,'R');
ChindGR2 = ChidelevitchModel.grRules;

for i = 1:size(bleh)
    if ~isempty(blehR{i})
        if isempty(bleh{i})
            count = 0;
            for j = 1:numel(blehR{i})
                if blehR{i}(j) == 1
                    ChindGR2{i} = ['(' ChindGR2{i}];
                else
                    ChindGR2{i} = [ChindGR2{i}(1:blehR{i}(j)+count-1) '(' ChindGR2{i}(blehR{i}(j)+count:end)];
                end
                count = count+1;
            end
        end
    end
end

bleh2=regexp(ChindGR2,')');
[mstart mend]=regexp(ChindGR2,'\w{2}[0-9]{4}');

for i = 1:size(bleh2)
    if ~isempty(mend{i})
        if isempty(bleh2{i})
            count = 0;
            for j = 1:numel(mend{i})
                c2 = 0;
                if mend{i}(j)+count < numel(ChindGR2{i}) 
                    if isequal(ChindGR2{i}(mend{i}(j)+count+1),'c') | isequal(ChindGR2{i}(mend{i}(j)+count+1),'A')
                        c2 = 1;
                    end
                end
                if mend{i}(j)+count+c2 == numel(ChindGR2{i})
                    ChindGR2{i} = [ChindGR2{i} ')'];
                else
                    ChindGR2{i} = [ChindGR2{i}(1:mend{i}(j)+c2+count) ')' ChindGR2{i}(mend{i}(j)+c2+count+1:end)];
                end
                count = count+1;
            end
        end
    end
end