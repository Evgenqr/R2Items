def createmonster(request, slug):
    slug = Location.objects.get(url=slug)   
    if request.method == 'POST':
        form = MonsterForm(request.POST, request.FILES)
        if form.is_valid():
            new_monster = form.save(commit=False)
            new_monster.save()
            new_monster.locations.add(slug)
    else:
        form = MonsterForm()
    return render(request, 'items/createmonster.html', {'form': form})



  
class EmailPostForm(forms.Form):  
    name = forms.CharField(max_length=25)  
    email = forms.EmailField()  
    to = forms.EmailField()  
    comments = forms.CharField(required=False,  
			       widget=forms.Textarea)





<tr><th><label for="id_item_img">Изображение:</label></th><td>
На данный момент: <a href="/media/media/items/6ed251f9cb32d5afe35501c97e6ac9e7.png">media/items/6ed251f9cb32d5afe35501c97e6ac9e7.png</a><br>
Изменить:
<input type="file" name="item_img" accept="image/*" id="id_item_img"></td></tr>
